"""
prepare_data.py (message detection)

Loads spam.csv (public UCI SMS Spam Collection), identifies the message
and label columns, removes duplicates, verifies class distribution and
absence of empty messages, and applies the shared clean_text() function.

IMPORTANT FRAMING NOTE:
This dataset is generic English SMS spam/ham. It is NOT a Bangladesh-
specific scam dataset and must never be described as one. We map:
    ham  -> legitimate/safe
    spam -> suspicious/spam
without claiming every "spam" message is financial fraud.

Run from project root:
    python -m ml.message_detection.prepare_data
"""

import os
import sys

import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from ml.message_detection.text_preprocessing import clean_text

RAW_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "spam.csv")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "artifacts", "message_processed.parquet")


def load_and_clean():
    df = pd.read_csv(RAW_PATH, encoding="cp1252")
    df = df[["v1", "v2"]].rename(columns={"v1": "label", "v2": "text"})

    print(f"Loaded {len(df)} raw rows.")

    before = len(df)
    df = df.drop_duplicates(subset=["text"]).reset_index(drop=True)
    print(f"Removed {before - len(df)} duplicate messages, {len(df)} remain.")

    empty_count = (df["text"].astype(str).str.strip() == "").sum()
    print(f"Empty/whitespace-only messages found: {empty_count}")
    df = df[df["text"].astype(str).str.strip() != ""].reset_index(drop=True)

    print("\nClass distribution after cleaning:")
    print(df["label"].value_counts())
    print(df["label"].value_counts(normalize=True))

    df["label_binary"] = (df["label"] == "spam").astype(int)  # 1 = spam/suspicious, 0 = ham/safe
    df["clean_text"] = df["text"].apply(clean_text)

    empty_after_clean = (df["clean_text"].str.strip() == "").sum()
    if empty_after_clean:
        print(f"WARNING: {empty_after_clean} messages became empty after cleaning; dropping them.")
        df = df[df["clean_text"].str.strip() != ""].reset_index(drop=True)

    return df


def main():
    df = load_and_clean()
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df[["text", "clean_text", "label", "label_binary"]].to_parquet(OUTPUT_PATH, index=False)
    print(f"\nSaved processed dataset ({len(df)} rows) to:\n{OUTPUT_PATH}")
    print("\nReminder: label_binary 1 = spam/suspicious, 0 = ham/safe. "
          "This is a generic public SMS spam corpus, NOT a Bangladesh-specific scam dataset.")


if __name__ == "__main__":
    main()
