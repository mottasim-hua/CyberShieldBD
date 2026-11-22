"""
train.py (message detection)

Trains Logistic Regression, Multinomial Naive Bayes, and Random Forest
on TF-IDF features of the cleaned spam.csv dataset.

TF-IDF is fit ONLY on the training split, then used to transform the
test split, to avoid preprocessing leakage.

Run from project root:
    python -m ml.message_detection.train
"""

import json
import os
import sys
import time

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

RANDOM_SEED = 42
DATA_PATH = os.path.join(os.path.dirname(__file__), "artifacts", "message_processed.parquet")
ARTIFACT_DIR = os.path.join(os.path.dirname(__file__), "artifacts")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")


def evaluate(model, X_test, y_test):
    pred = model.predict(X_test)
    return {
        "accuracy": float(accuracy_score(y_test, pred)),
        "precision": float(precision_score(y_test, pred)),
        "recall": float(recall_score(y_test, pred)),
        "f1_score": float(f1_score(y_test, pred)),
        "confusion_matrix": confusion_matrix(y_test, pred).tolist(),
    }


def main():
    df = pd.read_parquet(DATA_PATH)
    X_text = df["clean_text"]
    y = df["label_binary"]

    print(f"Loaded {len(df)} rows. Class distribution:\n{y.value_counts()}")

    X_train_text, X_test_text, y_train, y_test = train_test_split(
        X_text, y, test_size=0.2, random_state=RANDOM_SEED, stratify=y
    )

    # Fit TF-IDF ONLY on training text, then transform test text.
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        max_features=4000,
        min_df=2,
    )
    X_train = vectorizer.fit_transform(X_train_text)
    X_test = vectorizer.transform(X_test_text)
    print(f"TF-IDF vocabulary size: {len(vectorizer.vocabulary_)}")

    results = {}

    start = time.time()
    lr = LogisticRegression(max_iter=1000, random_state=RANDOM_SEED, class_weight="balanced")
    lr.fit(X_train, y_train)
    m = evaluate(lr, X_test, y_test)
    m["training_time_seconds"] = round(time.time() - start, 3)
    results["LogisticRegression"] = (m, lr)

    start = time.time()
    nb = MultinomialNB()
    nb.fit(X_train, y_train)
    m = evaluate(nb, X_test, y_test)
    m["training_time_seconds"] = round(time.time() - start, 3)
    results["MultinomialNB"] = (m, nb)

    start = time.time()
    rf = RandomForestClassifier(n_estimators=200, random_state=RANDOM_SEED, n_jobs=-1, class_weight="balanced")
    rf.fit(X_train, y_train)
    m = evaluate(rf, X_test, y_test)
    m["training_time_seconds"] = round(time.time() - start, 3)
    results["RandomForest"] = (m, rf)

    for name, (m, _) in results.items():
        print(f"\n{name}: {m}")

    best_name = max(results, key=lambda n: results[n][0]["f1_score"])
    best_metrics, best_model = results[best_name]
    print(f"\nSelected final model: {best_name} (F1={best_metrics['f1_score']:.4f})")

    os.makedirs(ARTIFACT_DIR, exist_ok=True)
    joblib.dump(best_model, os.path.join(ARTIFACT_DIR, "message_model.joblib"))
    joblib.dump(vectorizer, os.path.join(ARTIFACT_DIR, "tfidf_vectorizer.joblib"))

    metadata = {
        "selected_model": best_name,
        "label_meaning": {"1": "spam/suspicious", "0": "ham/safe"},
        "dataset": "UCI SMS Spam Collection (public, generic English SMS spam) via spam.csv",
        "dataset_limitation": (
            "This dataset is NOT Bangladesh-specific and does not represent "
            "bKash/Nagad/Rocket-style financial phishing. It is a general "
            "spam/ham corpus; 'spam' includes premium-rate/dating/prize spam, "
            "not exclusively financial fraud."
        ),
        "vectorizer": "TF-IDF, ngram_range=(1,2), max_features=4000, min_df=2, fit on train split only",
        "random_seed": RANDOM_SEED,
    }
    with open(os.path.join(ARTIFACT_DIR, "message_model_metadata.json"), "w") as f:
        json.dump(metadata, f, indent=2)

    os.makedirs(RESULTS_DIR, exist_ok=True)
    metrics_out = {name: m for name, (m, _) in results.items()}
    metrics_out["selected_model"] = best_name
    with open(os.path.join(RESULTS_DIR, "message_model_metrics.json"), "w") as f:
        json.dump(metrics_out, f, indent=2)

    print(f"\nSaved model artifacts to: {ARTIFACT_DIR}")
    print(f"Saved metrics to: {os.path.join(RESULTS_DIR, 'message_model_metrics.json')}")


if __name__ == "__main__":
    main()
