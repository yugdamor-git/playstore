from pathlib import Path
from apkpure_scraper import ApkpureScraper
from database import Database
from helper import generate_file_id

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
        
        pending_applications = list(self.db.application.find({"status":"pending"}))
        
        for application in pending_applications:
            package_url = application["package_url"]
            package_id = application["_id"]
            
            status,data = self.scraper.scrape_app_details(package_url)
            
            if status == False:
                self.db.update_application(package_id,{"error_count":application["error_count"] + 1})
                continue
            
            data["status"] = "active"
            
            package_name = application["package_name"]
            version = data["version"]
            version_code = data["version_code"]
            published_on = data["published_on_text"]
            download_page_url = data["download_page_url"]
            
            filename,file_id = generate_file_id(package_name,version,version_code,published_on)
            
            status,file_bytes,download_url = self.scraper.download_apk(download_page_url)
            
            if status == True:
                self.save_file(package_id,file_id,file_bytes)
                self.db.update_application(package_id,data)
                
                data["_id"] = file_id
                data["status"] = "active"
                data["filename"] = filename
                data["download_url"] = download_url
                
                self.db.add_file(data)
            else:
                self.db.update_application(package_id,{"error_count":application["error_count"] + 1})


if __name__ == "__main__":
    d = Downloader()
    d.process_pending_applications()
    

