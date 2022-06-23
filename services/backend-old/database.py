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
        
        self.packages = db["packages"]
        
        self.users = db["users"]
        
    def delete_app(self,package_id):
        
        self.version.delete_many(
            {"package_id":package_id}
        )
        
        self.apk.delete_many(
            {"package_id":package_id}
        )
        
        self.application.delete_one(
            {"_id":package_id}
        )
    
    def add_app(self,data):
        id = str(uuid.uuid4())
        now = datetime.now()
        data["_id"] = id
        data["status"] = "pending"
        data["description"] = ""
        data["created_at"] = now
        data["updated_at"] = now
        
        self.application.insert_one(data)
        
        return True
        
    
    def get_app_by_package_name(self,package_name):
        apps = list(self.application.find({"package_name":package_name}))
        return apps
    
    def get_recent_apps(self,limit):
        apps = list(self.application.find({}).sort("updated_at",pymongo.DESCENDING).limit(limit))
        return apps
    
    # def delete_app(self,id):
    #     self.update_app(id,{"status":"delete"})
    
    
    def update_app(self,id,data):
        now = datetime.now()
        data["updated_at"] = now
        self.application.update_one(
            {"_id":id},
            {
                "$set":data
            }
        )
    
    def find_app(self,keyword,limit):
        
        return list(self.application.find(
                {
                    "title":{
                        "$regex":keyword,
                        '$options' : 'i'
                    }
                }
            ).limit(limit))
        
    def get_app_details_by_id(self,id):
        app = list(self.application.find({"_id":id}))[0]
        
        versions = list(self.apk.find({
            "package_id":app["_id"]
        }).sort("uploaded_on_timestamp",pymongo.DESCENDING)
                        )
        
        app["versions"] = versions
        
        return app
    
    # def get_app(self,app_id):
    #     apps = list(self.apps.find({"app_id":app_id}))
        
    #     if len(apps) > 0:
    #         app_data = apps[0]
    #         return {
    #             "status":True,
    #             "app_data":app_data,
    #         }
        
    #     else:
    #         return {
    #             "status": False,
    #             "message":f"sorry, we don't have any data related to ({app_id})"
    #         }
    
    
    def generate_app_id(self,package_name,version,version_code):
        pn = str(package_name).strip().lower()
        v = str(version).strip().lower()
        vc = str(version_code).strip().lower()
        
        app_id = f'{pn}-{v}-{vc}'.replace(" ","-").strip()
        
        return app_id
    
    
    def insert_app(self,data):
        package_name = data["package_name"]
        version = data["version"]
        version_code = data["version_code"]
        
        app_id = self.generate_app_id(package_name,version,version_code)
        
        apps = list(self.apps.find({"app_id":app_id}))
        
        if len(apps) == 0:
            
            id = str(uuid.uuid4())
            tmp = data.copy()
            tmp["_id"] = id
            tmp["app_id"] = app_id
            
            self.apps.insert_one(tmp)
            
            apps = list(self.apps.find({"_id":id}))
            app_data = apps[0]
            
            
            return {
                "status":True,
                "app_data":app_data
            }
        
        else:
            return {
                "status": False,
                "message":f"sorry, we already have this app ({app_id})"
            }
    
    # def update_app(self,app_id,data):
    #     apps = list(self.apps.find({"app_id":app_id}))
        
    #     if len(apps) > 0:
    #         app_data = apps[0]
            
    #         self.apps.update_one({"_id":app_data["_id"]},{"$set":data})
            
    #         apps = list(self.apps.find({"_id":app_data["_id"]}))
            
    #         return {
    #             "status":True,
    #             "app_data":apps[0],
    #         }
        
    #     else:
    #         return {
    #             "status": False,
    #             "message":f"sorry, we don't have any data related to ({app_id})"
    #         }
    
    def insert_package(self,package_name,data):
        packages = list(self.packages.find({"package_name":package_name}))
        
        if len(packages) == 0:
            
            id = str(uuid.uuid4())
            tmp = data.copy()
            tmp["_id"] = id
            tmp["package_name"] = package_name
            self.packages.insert_one(tmp)
            
            packages = list(self.packages.find({"_id":id}))
            package_data = packages[0]
            apps = self.get_apps(package_name)
            
            return {
                "status":True,
                "package_data":package_data,
                "apps":apps
            }
        
        else:
            return {
                "status": False,
                "message":f"sorry, we already have this package ({package_name})"
            }
    
    def get_package(self,package_name):
        
        packages = list(self.packages.find({"package_name":package_name}))
        
        if len(packages) > 0:
            package_data = packages[0]
            apps = self.get_apps(package_name)
            return {
                "status":True,
                "package_data":package_data,
                "apps":apps
            }
        
        else:
            return {
                "status": False,
                "message":f"sorry, we don't have any data related to ({package_name})"
            }
    
    def update_package(self,package_name,data):
        
        packages = list(self.packages.find({"package_name":package_name}))
        
        if len(packages) > 0:
            package_data = packages[0]
            
            self.packages.update_one({"_id":package_data["_id"]},{"$set":data})
            packages = list(self.packages.find({"_id":package_data["_id"]}))
            apps = self.get_apps(package_name)
            
            return {
                "status":True,
                "package_data":packages[0],
                "apps":apps
            }
        
        else:
            return {
                "status": False,
                "message":f"sorry, we don't have any data related to ({package_name})"
            }