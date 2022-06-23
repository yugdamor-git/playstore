import json
from bs4 import BeautifulSoup
import cloudscraper
from helper import string_to_datetime

class ApkpureScraper:
    def __init__(self) -> None:
        
        self.wd = cloudscraper.create_scraper(browser={
        'browser': 'chrome',
        'platform': 'android',
        'desktop': False
        })
        
        self.max_retry = 20
        
        self.base_url = "https://apkpure.com"
        
        self.proxy = {
            "http":"http://108.59.14.203:13081",
            "https":"http://108.59.14.203:13081"
        }

        self.headers = {
        'authority': 'apkpure.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-US,en;q=0.9,ca;q=0.8,cs;q=0.7,fr;q=0.6,hi;q=0.5',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
        }

    def get_suggestions(self,keyword):
        url = f'https://m.apkpure.com/api/v1/search_suggestion_new?key={keyword}'
        
        data = []
        json_data = None
        for i in range(0,self.max_retry):
            response = self.wd.get(url)
            if response.status_code == 200:
                try:
                    json_data = response.json()
                    break
                except:
                    pass
        
        if json_data == None:
            return False,data
        
        for item in json_data:
            packageName = item.get("packageName",None)
            
            if packageName != None:
                s = {}
                s["package_name"] = packageName
                s["total_install"] = item.get("installTotal",None)
                s["icon_url"] = item.get("icon",None)
                s["title"] = item.get("title",None)
                s["package_url"] = "https://apkpure.com" + item.get("url","")
                
                s["tags"] = []
                
                for t in item.get("tags",[]):
                    s["tags"].append(t["name"])
                
                data.append(s)
        return True,data
    
    def scrape_app_details(self,url):
        soup = None
        data = {}
        
        for i in range(0,self.max_retry):
            response = self.wd.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text)
                break
            
        if soup == None:
            return False,data
        
        title = soup.find("div",{"class":"title-like"}).text.strip()

        download_btn = soup.find("div",{"id":"down_btns"})
        
        download_page_url = url + "/download?from=details"
        
        apk_version = download_btn.get("data-dt-version")
        
        version_code = download_btn.get("data-dt-versioncode")
        
        apk_size_bytes = download_btn.get("data-dt-filesize")
        
        apk_size_text = soup.find("span",{"class":"fsize"}).find("span").text

        published_on_text = soup.find("p",{"itemprop":"datePublished"}).text.strip()

        minimum_requirements = soup.find("strong",string="Requirements:").parent.parent.text.replace("Requirements:","").strip()

        data["title"] = title
        
        data["version"] = apk_version
        
        data["version_code"] = version_code
        
        data["size_bytes"] = apk_size_bytes
        
        data["size_text"] = apk_size_text
        
        data["published_on_text"] = published_on_text
        
        data["published_on_timestamp"] = string_to_datetime(published_on_text)
        
        data["minimum_requirements"] = minimum_requirements
        
        data["download_page_url"] = download_page_url
        
        return True,data
    
    def download_apk(self,url):
        error_message = "no error"
        soup = None
        for i in range(0,self.max_retry):
            try:
                response = self.wd.get(url,proxies=self.proxy,timeout=3)
                print(response.status_code)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text)
                    break
            except:
                pass
                
        if soup == None:
            error_message = "soup is none"
            return False,None,None,error_message

        download_link = soup.find("a",{"id":"download_link"}).get("href")
        
        file_bytes = None
        
        for i in range(0,self.max_retry):
            try:
                response = self.wd.get(download_link,proxies=self.proxy)
                print(response.status_code)
                if response.status_code == 200:
                    file_bytes = response.content
                    break
            except:
                pass
        
        if file_bytes == None:
            error_message = "file bytes are none"
            return False,None,download_link,error_message
        
        return True,file_bytes,download_link,error_message




if __name__ == "__main__":
    scraper = ApkpureScraper()
    
    # for i in scraper.get_suggestions("what"):
    #     print(i)
    
    # data = scraper.scrape_app_details("https://apkpure.com/facebook/com.facebook.katana")
    # print(data)
    
    # url = "https://apkpure.com/facebook/com.facebook.katana/download?from=details"
    
    # status,content = scraper.download_apk(url)
    
    # with open("test.apk","wb") as f:
    #     f.write(content)
    
    
    # https://download.apkpure.com/b/APK/Y29tLmZhY2Vib29rLmthdGFuYV8zMTQyMTQ0NTlfMWUyZjQ1MTU?_fn=RmFjZWJvb2tfdjM3MS4wLjAuMjQuMTA5X2Fwa3B1cmUuY29tLmFwaw&as=b9bb962ee431d4939163cda4ccd292ec62b49354&ai=1803426660&at=1656001244&_sa=ai%2Cat&k=26690eb5bf7af4b7f310a451cd175a9562b735dc&r=https%3A%2F%2Fapkpure.com%2Ffacebook%2Fcom.facebook.katana&_p=Y29tLmZhY2Vib29rLmthdGFuYQ&c=1%7CSOCIAL%7CZGV2PU1ldGElMjBQbGF0Zm9ybXMlMkMlMjBJbmMuJnQ9YXBrJnM9NTIzMzIxMzcmdm49MzcxLjAuMC4yNC4xMDkmdmM9MzE0MjE0NDU5&hot=1