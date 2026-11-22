from ml.url_detection.xai import explain_url
from ml.message_detection.xai import explain_message

def main():
 r=explain_url("http://192.168.0.1/login?verify=account")
 assert 0<=r["risk_score"]<=100 and r["top_factors"]
 m=explain_message("Congratulations! You won a free prize. Call now!")
 assert 0<=m["risk_score"]<=100 and m["top_factors"]
 print("XAI tests passed")
 print("URL:",r)
 print("MESSAGE:",m)
if __name__=="__main__": main()
