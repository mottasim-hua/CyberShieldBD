"""
prepare_data.py (URL detection)

Loads the raw PhiUSIIL CSV files, deduplicates by exact URL, regenerates
the 18 locked features FROM THE RAW URL STRING using
feature_extraction.extract_url_features (never copies the dataset's own
precomputed feature columns), and saves a compact processed dataset for
training.

Run from project root:
    python -m ml.url_detection.prepare_data
"""

import os
import sys
import time

import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from ml.url_detection.feature_extraction import extract_url_features, FEATURE_SCHEMA

PROJECT_ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
RAW_PART1 = os.path.join(PROJECT_ROOT, "data", "PhiUSIIL_Phishing_URL_Dataset_Part1.csv")
RAW_PART2 = os.path.join(PROJECT_ROOT, "data", "PhiUSIIL_Phishing_URL_Dataset_Part2.csv")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "artifacts", "url_processed.parquet")


def load_and_dedup():
    p1 = pd.read_csv(RAW_PART1)
    p2 = pd.read_csv(RAW_PART2)
    df = pd.concat([p1, p2], ignore_index=True)
    before = len(df)
    df = df.drop_duplicates(subset=["URL"]).reset_index(drop=True)
    after = len(df)
    print(f"Loaded {before} rows, {before - after} exact duplicate URLs removed, {after} rows remain.")
    return df


def generate_features(df: pd.DataFrame) -> pd.DataFrame:
    print("Regenerating all 18 features from the raw URL column (this does not copy dataset columns)...")
    start = time.time()
    records = [extract_url_features(u) for u in df["URL"]]
    feat_df = pd.DataFrame.from_records(records, columns=FEATURE_SCHEMA)
    elapsed = time.time() - start
    print(f"Feature generation for {len(df)} URLs took {elapsed:.1f}s.")
    return feat_df


def sanity_compare(original_df: pd.DataFrame, generated_df: pd.DataFrame):
    """
    Compare our independently regenerated features against the dataset's
    own precomputed columns (same names). We EXPECT small, systematic
    differences (e.g. off-by-one on length-style columns) because our
    extractor is a clean, from-scratch implementation, not a reproduction
    of the original authors' exact script. We report this rather than
    silently overwrite our own values.
    """
    print("\n--- Sanity comparison: regenerated features vs. original dataset columns ---")
    comparable_cols = [c for c in FEATURE_SCHEMA if c in original_df.columns]
    for col in comparable_cols:
        orig = original_df[col].reset_index(drop=True)
        gen = generated_df[col].reset_index(drop=True)
        diff = (gen - orig)
        exact_match_pct = (diff == 0).mean() * 100
        mean_diff = diff.mean()
        print(f"{col:30s} exact match: {exact_match_pct:5.1f}%   mean(generated - original): {mean_diff:+.3f}")


def main():
    df = load_and_dedup()

    print("\nLabel distribution:")
    print(df["label"].value_counts())
    print(df["label"].value_counts(normalize=True))

    feat_df = generate_features(df)
    sanity_compare(df, feat_df)

    processed = feat_df.copy()
    processed["Domain"] = df["Domain"].values  # kept ONLY for the domain-grouped split, not a model feature
    processed["label"] = df["label"].values

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    processed.to_parquet(OUTPUT_PATH, index=False)
    print(f"\nSaved processed dataset ({processed.shape[0]} rows, {processed.shape[1]} columns) to:\n{OUTPUT_PATH}")


if __name__ == "__main__":
    main()
