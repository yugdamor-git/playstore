from pathlib import Path
from apkpure_scraper import ApkpureScraper
from database import Database
from helper import generate_file_id,calc_timeout
import time

class Downloader:
    def __init__(self) -> None:
        self.scraper = ApkpureScraper()
        self.db = Database()
        self.downloads = Path("/downloads")
        
        

    def save_file(self,package_id,file_id,data_bytes):
        
        folder_path = self.downloads.joinpath(package_id)
        if not folder_path.exists():
            folder_path.mkdir()
        
        file_path = folder_path.joinpath(f'{file_id}.apk')
        
        if file_path.exists() == True:
            file_path.unlink()
            
        with open(file_path,"wb") as f:
            f.write(data_bytes)
    
    def process_pending_applications(self):
        
        pending_applications = list(self.db.files.find({"status":"downloading","error_count":{"$lt":10}}))
        
        for application in pending_applications:
            print(application)
            package_id = application["package_id"]
            app_download_url = application["app_download_url"]
            file_id = application["version_unique_id"]
            
            time_out = calc_timeout(application["size_bytes"])
            status,file_bytes,download_url,error_message = self.scraper.download_apk(app_download_url,time_out)
            print(download_url)
            print(error_message)
            if status == True:
                self.save_file(package_id,file_id,file_bytes)
                self.db.files.update_one({"_id":application["_id"]},{"$set":{"status":"active"}})
                
            else:
                self.db.files.update_one({"_id":application["_id"]},{"$set":{"error_count":application["error_count"] + 1}})
                


if __name__ == "__main__":
    max_run = 10
    for i in range(0,10):
        d = Downloader()
        d.process_pending_applications()
        time.sleep(2)
        

