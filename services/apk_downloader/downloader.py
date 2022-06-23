


from pathlib import Path
from database import Database
import cloudscraper

class ApkDownloader:
    def __init__(self) -> None:

        self.cwd = Path("/")
        
        self.db = Database()
        
        self.downloads = self.cwd.joinpath("downloads")
        
        self.current_id = None
        
        if not self.downloads.exists():
            self.downloads.mkdir()
            
        self.scraper = cloudscraper.create_scraper()
        
    
    def download(self,url,filename,foldername):
        folder_path = self.downloads.joinpath(foldername)
        
        if not folder_path.exists():
            folder_path.mkdir()
            
        file_path = folder_path.joinpath(filename)
        status = False
        # try:
        response = self.scraper.get(url)
        
        if response.status_code == 200:
            with open(file_path,"wb") as f:
                f.write(response.content)
            status = True
        else:
            status = False
            
            
        # except Exception as e:
        #     print(str(e))
        
        return status
    
if __name__ == "__main__":
    # testing
    ad = ApkDownloader()
    
    db = Database()
    
    for apk in list(db.apk.find({"status":"download"})):
        print(apk)
        # try:
        ext = None
        if apk["type"] == "APK" or apk["type"] == "apk":
            ext = "apk"
        else:
            ext = "xapk"
        
        filename = f'{apk["apk_unique_id"]}.{ext}'
        
        folder_name = apk["package_id"]
        
        download_url = apk["apk_download_url"]
        
        status = ad.download(download_url,filename,folder_name)
        
        update_item = {
                
                "local_file_name":filename,
            }
        
        if status == True:
            update_item["status"] = "active"
        
        db.update_apk(
            apk["_id"],
            update_item
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