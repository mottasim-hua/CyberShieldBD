# CyberShield BD — ML Pipelines (Current State)

Explainable AI-based detection of phishing URLs and spam/suspicious messages.
This package contains **only the ML layer** (Phases 1–4 of the project plan).
**Flask backend and React frontend are not built yet** — see "What's NOT here" below.

## Setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Get the datasets

The raw CSVs are **not included** in this package to keep it small. Copy your three
dataset files into a `data/` folder at the project root:

```
data/
  PhiUSIIL_Phishing_URL_Dataset_Part1.csv
  PhiUSIIL_Phishing_URL_Dataset_Part2.csv
  spam.csv
```

## Run everything (from the project root)

```bash
# URL detection
python -m ml.url_detection.prepare_data
python -m ml.url_detection.train
python -m ml.url_detection.tests.test_feature_extraction

# Message detection
python -m ml.message_detection.prepare_data
python -m ml.message_detection.train
```

Each `train.py` prints metrics to the console and writes them to
`ml/results/*_model_metrics.json`. Trained models and preprocessors are saved
under each module's `artifacts/` folder with `joblib`.

## What's here (verified, actually executed — not estimated)

### URL detection (`ml/url_detection/`)
- `feature_extraction.py` — `extract_url_features(url)`: the single shared function
  for all 18 locked, URL-string-only lexical features (no WHOIS, no crawling, no
  external APIs). This same function must be reused by the future Flask API.
- `prepare_data.py` — loads PhiUSIIL Part1+Part2, drops 425 exact-duplicate URLs
  (235,370 rows remain), regenerates all 18 features from the raw URL (never
  copies the dataset's own precomputed columns), sanity-compares the two.
- `train.py` — trains Logistic Regression, Random Forest, XGBoost. **Official
  evaluation is a domain-grouped 80/20 split** (no domain appears in both train
  and test — this was specifically validated to rule out domain-leakage inflating
  accuracy). A standard random split is also reported as a secondary reference.
- **Last actual run results (domain-grouped split):**

  | Model | Accuracy | Precision | Recall | F1 |
  |---|---|---|---|---|
  | Logistic Regression | 0.9859 | 0.9844 | 0.9913 | 0.9879 |
  | Random Forest | 0.9952 | 0.9945 | 0.9973 | 0.9959 |
  | **XGBoost (selected)** | **0.9954** | 0.9944 | 0.9977 | **0.9961** |

### Message detection (`ml/message_detection/`)
- `text_preprocessing.py` — shared text-cleaning function.
- `prepare_data.py` — loads `spam.csv` (UCI SMS Spam Collection), removes 403
  duplicate messages (5,169 remain), verifies class balance (ham 4,516 / spam 653).
- `train.py` — TF-IDF (fit on train split only) + Logistic Regression, Multinomial
  Naive Bayes, Random Forest.
- **Last actual run results:**

  | Model | Accuracy | Precision | Recall | F1 |
  |---|---|---|---|---|
  | **Logistic Regression (selected)** | **0.9816** | 0.9444 | 0.9084 | **0.9261** |
  | Multinomial Naive Bayes | 0.9691 | 1.0000 | 0.7557 | 0.8609 |
  | Random Forest | 0.9768 | 1.0000 | 0.8168 | 0.8992 |

  ⚠️ **This is a generic public English SMS spam dataset, not a Bangladesh-specific
  scam dataset.** Do not describe this model as "Bangladesh scam detection" in the
  report/demo — call it "Spam / Suspicious Message Detection" and state the
  limitation explicitly.

## What's NOT here yet

- Flask REST API (Phase 6)
- React frontend (Phase 2 / 7)
- SHAP or other explainability layer beyond model-native feature
  importance/coefficients (Phase 5)
- Any Bangladesh-specific dataset integration (none was available/downloadable
  during validation — see project conversation history for details)

## Known limitations (be upfront about these in the report/viva)

- URL model features exclude anything requiring webpage crawling, WHOIS, or
  external reputation APIs — by design, since the product must work from a
  pasted URL alone.
- `NoOfSubDomain`/TLD logic uses a simple "last label = TLD" rule (no public-suffix
  list), which slightly misclassifies multi-part TLDs like `co.uk` — documented,
  consistent at train and inference time.
- Message model's spam class is dominated by UK premium-rate/dating-service spam,
  not digital-payment phishing — framing this honestly matters for the viva.

## Reproducibility

- Python 3.12, random seed 42 throughout (`RANDOM_SEED = 42` in both `train.py`
  files).
- No hyperparameter search was performed — baseline, sensible parameters only,
  per project scope for a 5-day timeline.
