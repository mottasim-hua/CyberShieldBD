from __future__ import annotations
import os,joblib,numpy as np
BASE=os.path.dirname(__file__); ART=os.path.join(BASE,"artifacts")

def _load(): return joblib.load(os.path.join(ART,"message_model.joblib")),joblib.load(os.path.join(ART,"tfidf_vectorizer.joblib"))

def explain_message(message,top_k=5):
 model,vec=_load(); X=vec.transform([str(message)]); pred=int(model.predict(X)[0]); p=model.predict_proba(X)[0]; risk=float(p[1])*100.0
 names=vec.get_feature_names_out(); contrib=(X.toarray().ravel()*np.asarray(model.coef_[0])) if hasattr(model,"coef_") else np.zeros(X.shape[1]); idx=np.argsort(np.abs(contrib))[::-1]; factors=[]
 for i in idx:
  if contrib[i]==0: continue
  factors.append({"term":names[i],"contribution":float(contrib[i]),"direction":"suspicious" if contrib[i]>0 else "benign"})
  if len(factors)>=top_k: break
 return {"message":str(message),"prediction":pred,"label":"spam/suspicious" if pred==1 else "ham/safe","risk_score":round(risk,2),"top_factors":factors,"explanation":"The model highlights the terms that most influenced its decision."}
