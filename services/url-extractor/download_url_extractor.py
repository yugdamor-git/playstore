from database import Database
from playwright_driver import PlaywrightDriver

class DownloadUrlExtractor:
    def __init__(self) -> None:
        self.db = Database()
        self.wd = PlaywrightDriver()
        self.current_id = None
    
    
    def handle_response(self,response):
        url = response.url
        # print(url)
        if "https://download.apkpure.com" in url:
            download_url = response.headers["location"]
            print(download_url)
            self.db.application.update_one(
                {"_id":self.current_id},
                {
                    "$set":{
                        "status":"download",
                        "app_download_url":download_url
                    }
                }
            )
    
    def handle_routes(self,route):
        url = route.request.url
        
        if "https://m.apkpure.com" in url or "https://apkpure.com" in url:
            return route._continue()
        else:
            return route.abort()
    
    def main(self):
        
        pending_apps = list(self.db.application.find({"status":"pending","error_count":{"$lt":10}}))
        
        self.wd.start()
        
        self.wd.page.route("*/**",self.handle_routes)
        self.wd.page.on("response",self.handle_response)
        
        for app in pending_apps:
            print(app)
            try:
                self.db.update_application(app["_id"],{"error_count":app["error_count"] + 1})
                self.current_id = app["_id"]
                url = app["package_url"] + "/download?from=details"
                self.wd.page.goto(url)
            except Exception as e:
                print(str(e))
                
            
        self.wd.stop()
        

if __name__ == "__main__":
    due = DownloadUrlExtractor()
    due.main()