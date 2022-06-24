# url = "https://download.apkpure.com/b/APK/Y29tLndoYXRzYXBwXzIyMTQxMjAwNF9jYTkxZmNhMA?_fn=V2hhdHNBcHAgTWVzc2VuZ2VyX3YyLjIyLjE0LjEyX2Fwa3B1cmUuY29tLmFwaw&as=99ca774688802c93aea34ae60d008d7b62b4ab05&ai=1803426660&at=1656007309&_sa=ai%2Cat&k=3e14cebe6c4464e0e395e2145424100b62b74d8d&_p=Y29tLndoYXRzYXBw&c=1%7CCOMMUNICATION%7CZGV2PVdoYXRzQXBwJTIwTExDJnQ9YXBrJnM9NDA5OTgzOTMmdm49Mi4yMi4xNC4xMiZ2Yz0yMjE0MTIwMDQ&hot=1"

# from playwright_driver import PlaywrightDriver

# driver = PlaywrightDriver()

# driver.start()
# def handle(response):
#     url = response.url
#     if "https://download.apkpure.com" in url:
#         print(response.headers["location"])
        
# driver.page.on("response",handle)

# driver.page.goto(url)

# driver.stop()

from datetime import datetime
now = datetime.now()

t = now.timestamp
print(t)

# from itsdangerous import URLSafeTimedSerializer

# class TllToken:
#     def __init__(self) -> None:
#         self.secret_key = ""
#         self.salt = ""
#         self.time_to_live = 1 * 60
#         self.s = URLSafeTimedSerializer(self.secret_key,salt=self.salt.encode("utf-8"),max_age=self.time_to_live)
    
#     def generate_ttl_token(self,data):
#         token = self.s.dumps(data,)
#         return token

#     def decode_ttl_token(self,token):
#         data = self.s.loads(token)
#         return data