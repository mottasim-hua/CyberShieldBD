from __future__ import annotations
import os
from functools import lru_cache
import joblib
import numpy as np
import pandas as pd
from ml.url_detection.feature_extraction import FEATURE_SCHEMA, extract_url_features

BASE=os.path.dirname(__file__)
ART=os.path.join(BASE,"artifacts")

@lru_cache(maxsize=1)
def _load():
    model=joblib.load(os.path.join(ART,"url_model.joblib"))
    scaler_path=os.path.join(ART,"url_scaler.joblib")
    scaler=joblib.load(scaler_path) if os.path.exists(scaler_path) else None
    for name, transformer in (("model", model), ("scaler", scaler)):
        if transformer is None:
            continue
        feature_names=getattr(transformer,"feature_names_in_",None)
        if feature_names is not None and list(feature_names) != FEATURE_SCHEMA:
            raise ValueError(f"{name} feature names/order do not match FEATURE_SCHEMA")
        feature_count=getattr(transformer,"n_features_in_",len(FEATURE_SCHEMA))
        if feature_count != len(FEATURE_SCHEMA):
            raise ValueError(f"{name} expects {feature_count} features; expected {len(FEATURE_SCHEMA)}")
    return model,scaler

def _reason(name, value, contribution):
    # XGBoost contributions are toward class 1 (legitimate); negative values increase phishing risk.
    effect="increases" if contribution < 0 else "decreases" if contribution > 0 else "does not change"
    templates={
            "URLLength":f"URL length is {value}; its contribution {effect} phishing risk.",
            "DomainLength":f"Domain length is {value}; its contribution {effect} phishing risk.",
            "IsDomainIP":f"The raw-IP-address feature contribution {effect} phishing risk.",
            "TLDLength":f"TLD length is {value}; its contribution {effect} phishing risk.",
            "NoOfSubDomain":f"The subdomain-count feature ({value}) contribution {effect} phishing risk.",
            "NoOfLettersInURL":f"The letter-count feature ({value}) contribution {effect} phishing risk.",
            "LetterRatioInURL":f"The letter-ratio feature ({value:.2f}) contribution {effect} phishing risk.",
            "NoOfDegitsInURL":f"The digit-count feature ({value}) contribution {effect} phishing risk.",
            "DegitRatioInURL":f"The digit-ratio feature ({value:.2f}) contribution {effect} phishing risk.",
            "NoOfEqualsInURL":f"The equals-sign-count feature ({value}) contribution {effect} phishing risk.",
            "NoOfQMarkInURL":f"The question-mark-count feature ({value}) contribution {effect} phishing risk.",
            "NoOfAmpersandInURL":f"The ampersand-count feature ({value}) contribution {effect} phishing risk.",
            "NoOfOtherSpecialCharsInURL":f"The other-special-character count ({value}) contribution {effect} phishing risk.",
            "SpacialCharRatioInURL":f"The special-character ratio ({value:.2f}) contribution {effect} phishing risk.",
            "IsHTTPS":f"HTTPS is {'present' if value else 'not present'}; its contribution {effect} phishing risk.",
            "NoOfObfuscatedChar":f"The percent-encoded-character count ({value}) contribution {effect} phishing risk.",
            "ObfuscationRatio":f"The obfuscation ratio ({value:.2f}) contribution {effect} phishing risk.",
            "HasObfuscation":f"Percent-encoding obfuscation is {'present' if value else 'not present'}; its contribution {effect} phishing risk.",
    }
    return templates.get(name,f"The {name} feature contribution {effect} phishing risk.")


def _classify_status(prediction: int, phishing_probability: float) -> str:
    if prediction == 1:
        return "SAFE"
    return "DANGEROUS" if phishing_probability >= 80 else "SUSPICIOUS"


def explain_url(url, top_k=5):
    model,scaler=_load()
    feats=extract_url_features(url)
    X=pd.DataFrame([[feats[k] for k in FEATURE_SCHEMA]],columns=FEATURE_SCHEMA)
    Xin=scaler.transform(X) if scaler is not None else X
    pred=int(model.predict(Xin)[0])
    proba=model.predict_proba(Xin)[0]
    probability_by_class={int(label):float(probability) for label,probability in zip(model.classes_,proba)}
    if set(probability_by_class) != {0,1}:
        raise ValueError(f"Expected URL model classes 0 and 1; received {list(model.classes_)}")
    phishing_probability=probability_by_class[0]*100.0
    legitimate_probability=probability_by_class[1]*100.0
    risk=phishing_probability
    risk_score=risk
    if hasattr(model,"get_booster"):
        contrib=model.get_booster().predict(__import__('xgboost').DMatrix(Xin,feature_names=FEATURE_SCHEMA),pred_contribs=True)[0]
        vals=contrib[:-1]
    elif hasattr(model,"coef_"):
        vals=np.asarray(model.coef_[0]) * np.asarray(Xin[0])
    else:
        vals=np.zeros(len(FEATURE_SCHEMA))
    order=np.argsort(np.abs(vals))[::-1][:top_k]
    factors=[{"feature":FEATURE_SCHEMA[i],"value":feats[FEATURE_SCHEMA[i]],"contribution":float(vals[i]),"direction":"phishing" if vals[i] < 0 else "legitimate","explanation":_reason(FEATURE_SCHEMA[i],feats[FEATURE_SCHEMA[i]],float(vals[i]))} for i in order]
    status=_classify_status(pred, phishing_probability)
    prediction_label="phishing" if pred == 0 else "legitimate"
    explanation=f"The model predicts this URL is {prediction_label}. Estimated phishing risk is {risk_score:.6f}%; this is a model estimate, not certainty."
    return {
        "url": url,
        "prediction": pred,
        "label": "phishing" if pred == 0 else "legitimate",
        "phishing_probability": phishing_probability,
        "legitimate_probability": legitimate_probability,
        "risk_score": risk_score,
        "status": status,
        "top_factors": factors,
        "explanation": explanation,
    }
