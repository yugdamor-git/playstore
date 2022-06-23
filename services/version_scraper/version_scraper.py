
from gevent import monkey
monkey.patch_all()

from database import Database
from playwright_driver import PlaywrightDriver
from helper import create_unique_apk_id,find_value_by_text, string_to_datetime,get_apk_unique_id_from_url,extract_meta_data_from_url

class VersionScraper:
    
    def __init__(self) -> None:
        
        self.driver = PlaywrightDriver()
        
    
    def handle_route(self,route):
        url = route.request.url
        if "https://m.apkpure.com/" in str(url) or "https://apkpure.com/" in str(url):
            print(url)
            return route.continue_()
        else:
            return route.abort()
    
    def extract_version_info(self,soup):
        
        data = []
        
        version_wrap = soup.find("ul",{"class":"ver-wrap"})
        
        for item in version_wrap.find_all("li"):
            a_tag = item.find("a")
            title = a_tag.get("title",None)
            download_url = "https://apkpure.com" + a_tag.get("href")
            variant = None
            apk_unique_id = None
            version_code = None
            apk_type = None
            
            if "variant" in download_url:
                variant = True
            else:
                variant = False
            
            if variant == False:
                apk_unique_id,version_code,apk_type = extract_meta_data_from_url(download_url)
            
            uploaded_on = find_value_by_text(item,"Update on: ")
            min_android_version = find_value_by_text(item,"Requires Android: ")
            arch = find_value_by_text(item,"Architecture: ")
            size = find_value_by_text(item,"File Size: ")
            screen_dpi = find_value_by_text(item,"Screen DPI: ")
            
            version = item.find("span",{"class":"ver-item-n"}).text
            
            tmp = {}
            
            tmp["title"] = title
            tmp["version"] = version
            tmp["size"] = size
            tmp["version_code"] = version_code
            tmp["download_url"] = download_url
            tmp["apk_unique_id"] = apk_unique_id
            tmp["uploaded_on"] = uploaded_on
            tmp["uploaded_on_timestamp"] = string_to_datetime(uploaded_on)
            tmp["type"] = apk_type
            tmp["min_android_version"]= min_android_version
            tmp["arch"] = arch
            tmp["screen_dpi"] = screen_dpi
            tmp["variant"] = variant
            
            data.append(tmp)
            
        return data
    
    def extract_version_code_from_url(self,url):
        version_code = None
        try:
            version_code = url.split("/download/")[-1].split("-")[0]
        except Exception as e:
            print(f'error : {str(e)}')
        
        return version_code
            
    
    def extract_variant(self,item):
        data = []
        try:
            
            self.driver.page.goto(item["download_url"])
            
            soup = self.driver.get_soup()
            
            table = soup.find("div",{"class":"table"})
            
            for variant in table.find_all("div",{"class":"table-row"})[1:]:
                row_info = variant.find("div",{"class":"table-cell down"})
                
                updated_on = find_value_by_text(variant,"Update on: ")
                min_android_version = find_value_by_text(variant,"Requires Android: ")
                arch = find_value_by_text(variant,"Architecture: ")
                size = find_value_by_text(variant,"File Size: ")
                screen_dpi = find_value_by_text(variant,"Screen DPI: ")
                
                tmp = item.copy()
                
                a_tag = row_info.find("a")
                
                download_url = "https://apkpure.com" + a_tag.get("href")
                
                apk_unique_id,version_code,apk_type = extract_meta_data_from_url(download_url)
                
                title = a_tag.get("title")
                
                tmp["version_code"] = version_code
                tmp["size"] = size
                tmp["download_url"] = download_url
                tmp["title"] = title
                tmp["arch"] = arch
                tmp["min_android_version"] = min_android_version
                tmp["screen_dpi"] = screen_dpi
                tmp["uploaded_on"] = updated_on
                tmp["uploaded_on_timestamp"] = string_to_datetime(updated_on)
                tmp["apk_unique_id"] = apk_unique_id
                tmp["type"] = apk_type
                
                data.append(tmp)
        except Exception as e:
            print(f'error : {str(e)}')
        
        return data
    
    def scrape(self,url):
        data = []
        self.driver.start()
        
        try:
            
            self.driver.page.route("**/*",self.handle_route)
            
            self.driver.page.goto(url)
            
            soup = self.driver.get_soup()
            
            versions = self.extract_version_info(soup)
            
            for v in versions:
                if v["variant"] == True:
                    for item in self.extract_variant(v):
                        data.append(item)
                else:
                    data.append(v)
        except Exception as e:
            print(f'error : {str(e)}')
        
        self.driver.stop()
        
        return data
    
    

if __name__ == "__main__":
    vs = VersionScraper()
    
    db = Database()
    
    for app in db.get_pending_app():
        id = app["_id"]
        url = app["package_url"]
        package_name = app["package_name"]
        
        version_url = url + "/versions"
        
        data = vs.scrape(version_url)
        
        for apk in data:
            version = apk["version"]
            
            version_id = db.add_version(version,package_name,id)
            
            version_code = apk["version_code"]
            
            apk_type = apk["type"]
            
            tmp = apk.copy()
            
            tmp["status"] = "pending"
            
            tmp["version_id"] = version_id
            
            tmp["package_name"] = package_name
            
            tmp["package_id"] = id
            
            tmp["error_count"] = 0
            
            tmp["sftp_status"] = False
            
            tmp["apk_id"] = create_unique_apk_id(package_name,version,version_code,apk_type)
            
            apk_id = db.add_apk(tmp)
            
            print(f'apk added : {apk_id}')
            
        db.update_app_status("active",app["_id"])