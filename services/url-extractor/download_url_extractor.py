from database import Database
from playwright_driver import PlaywrightDriver

class DownloadUrlExtractor:
    def __init__(self) -> None:
        self.db = Database()
        self.wd = PlaywrightDriver()
        self.current_id = None
    
    
    def handle_response(self,response):
        url = response.url
        if "https://download.apkpure.com" in url:
            download_url = response.headers["location"]
            
            self.db.application.update_one(
                {"_id":self.current_id},
                {
                    "$set":{
                        "status":"download",
                        "app_download_url":download_url
                    }
                }
            )
            
    
    def main(self):
        
        pending_apps = list(self.db.application.find({"status":"pending"}))
        self.wd.start()
        for app in pending_apps:
            self.current_id = app["_id"]
            url = app["download_page_url"]
            self.wd.page.on("response",)
            self.wd.page.goto(url)
        self.wd.stop()
        

if __name__ == "__main__":
    due = DownloadUrlExtractor()
    due.main()