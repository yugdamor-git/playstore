from datetime import datetime
import uuid
import pymongo
import os

user = os.environ.get("MONGO_USERNAME") 
password = os.environ.get("MONGO_PASSWORD")
host = "mongodb:27017"

class Database:
    def __init__(self):
        db_name = "playstore"
        connection_uri = f'mongodb://{user}:{password}@{host}/?authSource=admin'
        # connection_uri = f'mongodb://{host}/?authSource=admin'
        
        client = pymongo.MongoClient(connection_uri)
        
        db = client[db_name]
        
        self.application = db["application"]
        
        self.version = db["version"]
        
        self.apk = db["apk"]
        
        self.users = db["users"]
    
    def update_app_status(self,status,id):
        now = datetime.now()
        
        self.application.update_one(
            {"_id":id},
            {
                "$set":{
                "updated_at":now,
                "status":status
            }
            }
        )
    
    def get_pending_app(self):
        
        apps = list(self.application.find({"status":"pending"}))
        
        return apps
    
    
    def get_version(self,version,package_name,package_id):
        
        version = list(self.version.find(
            {
                "version":version,
                "package_name":package_name,
                "package_id":package_id
            }
        ))
        
        return version
    
    def add_version(self,version,package_name,package_id):
        now = datetime.now()
        versions = self.get_version(version,package_name,package_id)
        
        if len(versions) > 0:
            return versions[0]["_id"]
        else:
            id = str(uuid.uuid4())
            
            self.version.insert_one(
                {
                    "_id":id,
                    "version":version,
                    "package_name":package_name,
                    "package_id":package_id,
                    "created_at":now,
                    "updated_at":now
                }
            )
            
            return id
    
    def find_apk(self,apk_id):
        
        apks = list(self.apk.find({"apk_unique_id":apk_id}))
        
        return apks
    
    def add_apk(self,data):
        now = datetime.now()
        apk_id = data["apk_unique_id"]
        
        apks = self.find_apk(apk_id)
        
        if len(apks) > 0:
            return apks[0]["_id"]
        else:
            id = str(uuid.uuid4())
            data["_id"] = id
            data["updated_at"] = now
            data["created_at"] = now
            self.apk.insert_one(data)
            return id
            
            