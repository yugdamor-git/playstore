from datetime import datetime
from pathlib import Path

import pymongo
import os
import shutil

from helper import generate_sha1_hex,get_current_timestamp

user = os.environ.get("MONGO_USERNAME")
password = os.environ.get("MONGO_PASSWORD")
host = "localhost:27020"

class Database:
    def __init__(self):
        db_name = "playstore"
        connection_uri = f'mongodb://{user}:{password}@{host}/?authSource=admin'
        # connection_uri = f'mongodb://{host}/?authSource=admin'
        
        client = pymongo.MongoClient(connection_uri)
        
        db = client[db_name]
        
        self.application = db["application"]
        
        self.version = db["version"]
        
        self.files = db["files"]
        
        self.downloads = Path('/downloads')
    
    def _get_application_by_package(self,package_name):
        
        apps = list(self.application.find({"package_name":package_name}))
        
        return apps
    
    def add_application(self,data):
        
        package_name = data["package_name"]
        
        apps = self._get_application_by_package(package_name)
        
        if len(apps) > 0:
            return False,apps[0]["_id"],"we already have this app in our database"
        
        id = generate_sha1_hex(package_name)
        
        data["_id"] = id
        data["created_at"] = get_current_timestamp()
        data["updated_at"] = get_current_timestamp()
        data["status"] = "pending"
        data["error_count"] = 0
        
        self.application.insert_one(data)
        
        return True,id,"application added into database."
    
    def delete_application(self,package_id):
        status = False
        message = "all application data is deleted"
        try:
            self.files.delete_many(
                {"package_id":package_id}
            )
            
            self.version.delete_many(
                {
                    "package_id":package_id
                }
            )
            
            self.application.delete_one(
                {
                    "_id":package_id
                }
            )
            
            # delete folder
            
            folder_path = self.downloads.joinpath(package_id)
            
            shutil.rmtree(folder_path)
            status = True
        except Exception as e:
            message = str(e)
            status = False
        
        return status,message
        
    def update_application(self,package_id,data):
        data["updated_at"] = get_current_timestamp()
        self.application.update_one(
            {"_id":package_id},
            {
                "$set":data
            }
        )
    
    def get_recent_application(self,limit):
        apps = list(
            self.application.find({}).sort("updated_at",pymongo.DESCENDING).limit(limit)
        )
        
        return apps
    def _get_application_by_package_id(self,package_id):
        apps = list(self.application.find({"_id":package_id}))
        return apps
    def get_application_details(self,package_id):
        
        app = self._get_application_by_package_id()
        
        if len(app) > 0:
            return False,None
        
        application_details = app[0]
        
        application_version = list(self.version.find({"package_id":package_id}).sort("updated_at",pymongo.DESCENDING))
        
        application_files = list(self.files.find({"package_id":package_id}).sort("published_on_timestamp",pymongo.DESCENDING))
        
        application_details["versions"] = application_version
        
        application_details["files"] = application_files
        
        return True,application_details
    
    def add_file(self,data):
        data["created_at"] = get_current_timestamp()
        data["updated_at"] = get_current_timestamp()
        try:
            self.files.insert_one(data)
            return True
        except:
            return False
        