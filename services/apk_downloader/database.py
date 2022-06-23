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
    
   
    def get_pending_apk(self):
        apks = list(self.apk.find({
            "status":"pending"
        }))
        
        return apks
    
    def update_apk(self,id,data):
        
        self.apk.update_one(
            {"_id":id},
            {
                "$set":data
            }
        )
    