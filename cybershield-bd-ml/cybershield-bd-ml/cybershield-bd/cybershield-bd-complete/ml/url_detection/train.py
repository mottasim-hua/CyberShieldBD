
import json
import os
import sys
import time

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import GroupShuffleSplit, train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from ml.url_detection.feature_extraction import FEATURE_SCHEMA

RANDOM_SEED = 42
DATA_PATH = os.path.join(os.path.dirname(__file__), "artifacts", "url_processed.parquet")
ARTIFACT_DIR = os.path.join(os.path.dirname(__file__), "artifacts")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")


def load_data():
    df = pd.read_parquet(DATA_PATH)
    X = df[FEATURE_SCHEMA].copy()
    y = df["label"].copy()
    groups = df["Domain"].copy()
    return X, y, groups


def make_splits(X, y, groups):
    # Official split: domain-grouped, 80/20
    gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=RANDOM_SEED)
    train_idx, test_idx = next(gss.split(X, y, groups=groups))
    grouped_split = (
        X.iloc[train_idx], X.iloc[test_idx],
        y.iloc[train_idx], y.iloc[test_idx],
    )
    train_domains = set(groups.iloc[train_idx])
    test_domains = set(groups.iloc[test_idx])
    overlap = train_domains & test_domains
    print(f"[Domain-grouped split] domains in both train & test: {len(overlap)} (should be 0)")

    # Secondary reference split: standard stratified random 80/20
    X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_SEED, stratify=y
    )
    random_split = (X_train_r, X_test_r, y_train_r, y_test_r)

    return grouped_split, random_split


def evaluate(model, X_test, y_test):
    pred = model.predict(X_test)
    return {
        "accuracy": float(accuracy_score(y_test, pred)),
        "precision": float(precision_score(y_test, pred)),
        "recall": float(recall_score(y_test, pred)),
        "f1_score": float(f1_score(y_test, pred)),
        "confusion_matrix": confusion_matrix(y_test, pred).tolist(),
    }


def train_and_eval_all(X_train, X_test, y_train, y_test, scale_for_lr=True):
    results = {}

    # --- Logistic Regression (scaled) ---
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    start = time.time()
    lr = LogisticRegression(max_iter=1000, random_state=RANDOM_SEED)
    lr.fit(X_train_scaled, y_train)
    lr_time = time.time() - start
    lr_metrics = evaluate(lr, X_test_scaled, y_test)
    lr_metrics["training_time_seconds"] = round(lr_time, 3)
    results["LogisticRegression"] = (lr_metrics, lr, scaler)

    # --- Random Forest (no scaling needed) ---
    start = time.time()
    rf = RandomForestClassifier(n_estimators=200, random_state=RANDOM_SEED, n_jobs=-1)
    rf.fit(X_train, y_train)
    rf_time = time.time() - start
    rf_metrics = evaluate(rf, X_test, y_test)
    rf_metrics["training_time_seconds"] = round(rf_time, 3)
    results["RandomForest"] = (rf_metrics, rf, None)

    # --- XGBoost (no scaling needed) ---
    start = time.time()
    xgb = XGBClassifier(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.1,
        random_state=RANDOM_SEED,
        eval_metric="logloss",
        n_jobs=-1,
    )
    xgb.fit(X_train, y_train)
    xgb_time = time.time() - start
    xgb_metrics = evaluate(xgb, X_test, y_test)
    xgb_metrics["training_time_seconds"] = round(xgb_time, 3)
    results["XGBoost"] = (xgb_metrics, xgb, None)

    return results


def main():
    X, y, groups = load_data()
    print(f"Loaded {len(X)} rows, {len(FEATURE_SCHEMA)} features.")
    print("Class distribution:\n", y.value_counts())

    (Xg_tr, Xg_te, yg_tr, yg_te), (Xr_tr, Xr_te, yr_tr, yr_te) = make_splits(X, y, groups)

    print("\n=== Training on OFFICIAL domain-grouped split ===")
    grouped_results = train_and_eval_all(Xg_tr, Xg_te, yg_tr, yg_te)

    print("\n=== Training on SECONDARY standard random split (robustness reference) ===")
    random_results = train_and_eval_all(Xr_tr, Xr_te, yr_tr, yr_te)

    for name, (metrics, _, _) in grouped_results.items():
        print(f"\n[grouped] {name}: {metrics}")
    for name, (metrics, _, _) in random_results.items():
        print(f"[random]  {name}: {metrics}")

    # ---- Model selection: based on OFFICIAL (grouped) split F1 ----
    best_name = max(grouped_results, key=lambda n: grouped_results[n][0]["f1_score"])
    best_metrics, best_model, best_scaler = grouped_results[best_name]
    print(f"\nSelected final model: {best_name} (F1={best_metrics['f1_score']:.4f} on grouped split)")

    # ---- Save artifacts ----
    os.makedirs(ARTIFACT_DIR, exist_ok=True)
    joblib.dump(best_model, os.path.join(ARTIFACT_DIR, "url_model.joblib"))
    if best_scaler is not None:
        joblib.dump(best_scaler, os.path.join(ARTIFACT_DIR, "url_scaler.joblib"))

    metadata = {
        "selected_model": best_name,
        "feature_schema": FEATURE_SCHEMA,
        "requires_scaling": best_scaler is not None,
        "label_meaning": {"1": "Legitimate", "0": "Phishing"},
        "evaluation_split": "domain-grouped (GroupShuffleSplit, test_size=0.2, random_state=42)",
        "random_seed": RANDOM_SEED,
    }
    with open(os.path.join(ARTIFACT_DIR, "url_model_metadata.json"), "w") as f:
        json.dump(metadata, f, indent=2)

    # ---- Save metrics (both splits) ----
    os.makedirs(RESULTS_DIR, exist_ok=True)
    metrics_out = {
        "domain_grouped_split": {name: m for name, (m, _, _) in grouped_results.items()},
        "standard_random_split_reference": {name: m for name, (m, _, _) in random_results.items()},
        "selected_model": best_name,
    }
    with open(os.path.join(RESULTS_DIR, "url_model_metrics.json"), "w") as f:
        json.dump(metrics_out, f, indent=2)

    print(f"\nSaved model artifacts to: {ARTIFACT_DIR}")
    print(f"Saved metrics to: {os.path.join(RESULTS_DIR, 'url_model_metrics.json')}")


if __name__ == "__main__":
    main()
