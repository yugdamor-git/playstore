from itsdangerous import URLSafeTimedSerializer
import os

class TllToken:
    def __init__(self) -> None:
        self.secret_key = os.environ.get("SECRET_KEY")
        self.salt = "apk.file.download"
        self.time_to_live = 1 * 60
        self.s = URLSafeTimedSerializer(self.secret_key,salt=self.salt.encode("utf-8"),expires_in=self.time_to_live)
    
    def generate_ttl_token(self,data):
        token = self.s.dumps(data,)
        return token

    def decode_ttl_token(self,token):
        data = self.s.loads(token)
        return data