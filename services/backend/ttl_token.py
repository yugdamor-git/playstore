from itsdangerous import URLSafeTimedSerializer
import os
from datetime import datetime
class TllToken:
    def __init__(self) -> None:
        self.secret_key = os.environ.get("SECRET_KEY")
        self.salt = "apk.file.download"
        self.time_to_live = 1 * 60
        self.s = URLSafeTimedSerializer(self.secret_key,salt=self.salt.encode("utf-8"))
        self.default_redirect_on_expire = "https://latestmodapks.com"
    
    def generate_ttl_token(self,data):
        timestamp = datetime.now()
        data["timestamp"] = timestamp.timestamp()
        token = self.s.dumps(data,)
        return token

    def decode_ttl_token(self,token):
        data = self.s.loads(token)
        data["timestamp"] = datetime.fromtimestamp(data["timestamp"])
        if not "redirect" in data:
            data["redirect"] = self.default_redirect_on_expire
        now = datetime.now()
        
        seconds = (now - data["timestamp"]).seconds
        if seconds > self.time_to_live:
            data["status"] = False
        else:
            data["status"] = True 
        
        return data