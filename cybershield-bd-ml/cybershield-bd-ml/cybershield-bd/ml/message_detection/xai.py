from __future__ import annotations
import os,joblib,numpy as np
from functools import lru_cache
from ml.message_detection.text_preprocessing import clean_text
from ml.risk_levels import risk_level
BASE=os.path.dirname(__file__); ART=os.path.join(BASE,"artifacts")

@lru_cache(maxsize=1)
def _load(): return joblib.load(os.path.join(ART,"message_model.joblib")),joblib.load(os.path.join(ART,"tfidf_vectorizer.joblib"))

def explain_message(message,top_k=5):
 model,vec=_load(); X=vec.transform([clean_text(message)]); pred=int(model.predict(X)[0]); p=model.predict_proba(X)[0]
 probability_by_class={int(label):float(probability) for label,probability in zip(model.classes_,p)}
 if set(probability_by_class)!={0,1}: raise ValueError(f"Expected message model classes 0 and 1; received {list(model.classes_)}")
 spam_probability=probability_by_class[1]*100.0; ham_probability=probability_by_class[0]*100.0; risk=round(spam_probability,2); status=risk_level(risk)
 names=vec.get_feature_names_out(); contrib=(X.toarray().ravel()*np.asarray(model.coef_[0])) if hasattr(model,"coef_") else np.zeros(X.shape[1]); idx=np.argsort(np.abs(contrib))[::-1]; factors=[]
 for i in idx:
  if contrib[i]==0: continue
  factors.append({"term":names[i],"contribution":float(contrib[i]),"direction":"suspicious" if contrib[i]>0 else "benign"})
  if len(factors)>=top_k: break
 label="spam/suspicious" if pred==1 else "ham/safe"
 level_label=status.lower().replace("_", " ")
 return {"message":str(message),"prediction":pred,"label":label,"spam_probability":round(spam_probability,2),"ham_probability":round(ham_probability,2),"risk_score":risk,"status":status,"top_factors":factors,"explanation":f"The model predicts {label}; its spam probability is {risk:.2f}% (risk level: {level_label}). The listed terms show the strongest model influences."}
