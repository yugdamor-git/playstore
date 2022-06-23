


from pathlib import Path
from database import Database
from playwright_driver import PlaywrightDriver


class ApkDownloader:
    def __init__(self) -> None:
        
        self.driver = PlaywrightDriver()

        self.cwd = Path("/")
        
        self.downloads = self.cwd.joinpath("downloads")
        
        if not self.downloads.exists():
            self.downloads.mkdir()
        
    def download(self,url,file_name,id):
        
        folder_path = self.downloads.joinpath(id)
        
        if not folder_path.exists():
            folder_path.mkdir()
            
        file_path = folder_path.joinpath(file_name)
        if self.init_download(url,file_path) == True:
            print(f'download_successful')
        else:
            print(f'download_failed')
        
    
    def handle_download(self,route):
        url = route.request.url
        if "download.apkpure.com" in str(url) or "https://m.apkpure.com/" in str(url) or "https://apkpure.com/" in str(url):
            return route.continue_()
        
        else:
            return route.abort()
    
    def init_download(self,url,file_path):
        
        self.driver.start()
        status = False
        try:
            self.driver.page.route("**/*",self.handle_download)
            
            with self.driver.page.expect_download() as download_info:
                self.driver.page.goto(url)
            
            file = download_info.value
            
            file.save_as(file_path)
            
            status = True
        except Exception as e:
            print(f'error : {str(e)}')
            
        self.driver.stop()
        
        return status


if __name__ == "__main__":
    # testing
    ad = ApkDownloader()
    
    db = Database()
    
    for apk in db.get_pending_apk():
        print(apk)
        # try:
        ext = None
        if apk["type"] == "APK" or apk["type"] == "apk":
            ext = "apk"
        else:
            ext = "zip"
        
        filename = f'{apk["apk_unique_id"]}.{ext}'
        
        folder_name = apk["package_id"]
        
        download_url = apk["download_url"]
        
        ad.download(download_url,filename,folder_name)
        
        db.update_apk(
            apk["_id"],
            {
                "status":"active",
                "local_file_name":filename
            }
        )
        # except Exception as e:
            
        #     error_count = apk["error_count"] + 1
                
        #     db.update_apk(
        #         apk["_id"],
        #         {
        #             "error_count":error_count,
        #             "error_message":str(e)
        #         }
        #     )
    
    # file_name = "test.apk"
    # id = "whatsapp"
    # url = "https://m.apkpure.com/whatsapp-messenger/com.whatsapp/download/221304004-APK-8d9ca51fd6ef0bcfa6c7f359c0f681b7?from=variants%2Fversion"
    # ad.download(url,file_name,id)