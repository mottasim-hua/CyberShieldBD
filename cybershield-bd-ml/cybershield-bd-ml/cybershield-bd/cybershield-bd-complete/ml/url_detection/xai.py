from __future__ import annotations
import json, os
import joblib
import numpy as np
import pandas as pd
from ml.url_detection.feature_extraction import FEATURE_SCHEMA, extract_url_features

BASE=os.path.dirname(__file__)
ART=os.path.join(BASE,"artifacts")

def _load():
    model=joblib.load(os.path.join(ART,"url_model.joblib"))
    scaler_path=os.path.join(ART,"url_scaler.joblib")
    scaler=joblib.load(scaler_path) if os.path.exists(scaler_path) else None
    return model,scaler

def _reason(name, value, contribution):
    direction="phishing" if contribution>0 else "legitimate"
    templates={
      "URLLength":f"URL length is {value}, which contributes toward {direction} risk.",
      "DomainLength":f"Domain length is {value}, which contributes toward {direction} risk.",
      "IsDomainIP":f"The URL uses a raw IP address, which contributes toward {direction} risk.",
      "TLDLength":f"TLD length is {value}, contributing toward {direction} risk.",
      "NoOfSubDomain":f"The URL contains {value} subdomain level(s), contributing toward {direction} risk.",
      "NoOfLettersInURL":f"The URL contains {value} letters, contributing toward {direction} risk.",
      "LetterRatioInURL":f"Letter ratio is {value:.2f}, contributing toward {direction} risk.",
      "NoOfDegitsInURL":f"The URL contains {value} digit(s), contributing toward {direction} risk.",
      "DegitRatioInURL":f"Digit ratio is {value:.2f}, contributing toward {direction} risk.",
      "NoOfEqualsInURL":f"The URL contains {value} '=' character(s), contributing toward {direction} risk.",
      "NoOfQMarkInURL":f"The URL contains {value} question mark(s), contributing toward {direction} risk.",
      "NoOfAmpersandInURL":f"The URL contains {value} '&' character(s), contributing toward {direction} risk.",
      "NoOfOtherSpecialCharsInURL":f"The URL contains {value} other special character(s), contributing toward {direction} risk.",
      "SpacialCharRatioInURL":f"Special-character ratio is {value:.2f}, contributing toward {direction} risk.",
      "IsHTTPS":f"HTTPS is {'present' if value else 'not present'}, contributing toward {direction} risk.",
      "NoOfObfuscatedChar":f"The URL contains {value} percent-encoded sequence(s), contributing toward {direction} risk.",
      "ObfuscationRatio":f"Obfuscation ratio is {value:.2f}, contributing toward {direction} risk.",
      "HasObfuscation":f"Percent-encoding obfuscation is {'present' if value else 'not present'}, contributing toward {direction} risk.",
    }
    return templates.get(name,f"{name}={value} contributes toward {direction} risk.")

def explain_url(url, top_k=5):
    model,scaler=_load()
    feats=extract_url_features(url)
    X=pd.DataFrame([[feats[k] for k in FEATURE_SCHEMA]],columns=FEATURE_SCHEMA)
    Xin=scaler.transform(X) if scaler is not None else X
    pred=int(model.predict(Xin)[0])
    proba=model.predict_proba(Xin)[0]
    # label 0 = phishing, 1 = legitimate
    risk=float(proba[0])*100.0
    if hasattr(model,"get_booster"):
        contrib=model.get_booster().predict(__import__('xgboost').DMatrix(Xin,feature_names=FEATURE_SCHEMA),pred_contribs=True)[0]
        vals=contrib[:-1]
    elif hasattr(model,"coef_"):
        vals=np.asarray(model.coef_[0]) * np.asarray(Xin[0])
    else:
        vals=np.zeros(len(FEATURE_SCHEMA))
    order=np.argsort(np.abs(vals))[::-1][:top_k]
    factors=[{"feature":FEATURE_SCHEMA[i],"value":feats[FEATURE_SCHEMA[i]],"contribution":float(vals[i]),"explanation":_reason(FEATURE_SCHEMA[i],feats[FEATURE_SCHEMA[i]],float(vals[i]))} for i in order]
    status="Phishing / Dangerous" if risk>=50 else "Likely Legitimate"
    return {"url":url,"prediction":pred,"label":"phishing" if pred==0 else "legitimate","risk_score":round(risk,2),"status":status,"top_factors":factors,"explanation":("The URL has characteristics that increase phishing risk." if risk>=50 else "The URL has characteristics that are more consistent with legitimate URLs.")}
