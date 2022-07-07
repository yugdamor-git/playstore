import json
from bs4 import BeautifulSoup
import cloudscraper
from helper import string_to_datetime
import os


class ApkpureScraper:
    def __init__(self) -> None:

        self.wd = cloudscraper.create_scraper()

        self.max_retry = 3

        self.base_url = "https://apkpure.com"
        
        proxy = os.environ.get("PROXY")
        
        self.proxy = {
            "http":f'http://{proxy}',
            "https":f'http://{proxy}'
        }

    def get_suggestions(self, keyword):
        url = f'https://m.apkpure.com/api/v1/search_suggestion_new?key={keyword}'

        data = []
        json_data = None
        for i in range(0, self.max_retry):
            response = self.wd.get(url)
            if response.status_code == 200:
                try:
                    json_data = response.json()
                    break
                except:
                    pass

        if json_data == None:
            return False, data

        for item in json_data:
            packageName = item.get("packageName", None)

            if packageName != None:
                s = {}
                s["package_name"] = packageName
                s["total_install"] = item.get("installTotal", None)
                s["icon_url"] = item.get("icon", None)
                s["title"] = item.get("title", None)
                s["package_url"] = "https://apkpure.com" + item.get("url", "")

                s["tags"] = []

                for t in item.get("tags", []):
                    s["tags"].append(t["name"])

                data.append(s)
        return True, data
    def extract_suggestions_v2(self,soup):
        apps = []
        
        try:
            first = soup.find("div",{"class":"first"})
            a_tag = first.find("a",{"class":"first-info"})
            title = first.find("div",{"class":"info"}).find("p").text.strip()
            img_tag = first.find("img")
            package_name = first.get("data-dt-app")
            total_install = None
            icon_url = None
            
            if img_tag != None:
                icon_url = img_tag.get("src")
            tags = []
            
            package_url = "https://apkpure.com" + a_tag.get("href")
            
            apps.append({
                "package_name":package_name,
                "total_install":total_install,
                "icon_url":icon_url,
                "title":title,
                "package_url":package_url,
                "tags":tags,
            })
            
        except:
            pass
        try:
            list_app = soup.find("div",{"class":"list app-list"}).find("ul")
            
            for app in list_app.find("li"):
                try:
                    a_tag = app.find("a")
                    
                    href = a_tag.get("href")
                    
                    package_name = href.split("/")[-1]
                    
                    package_url = "https://apkpure.com" + href
                    
                    icon_url = a_tag.find("img").get("src")
                    
                    title = a_tag.find("div",{"class":"r"}).find("p").text.strip()
                    
                    tags = []
                    
                    total_install = None
                    
                    apps.append({
                    "package_name":package_name,
                    "total_install":total_install,
                    "icon_url":icon_url,
                    "title":title,
                    "package_url":package_url,
                    "tags":tags,
                    })
                except Exception as e:
                    print(f'error : {str(e)}')
        except:
            pass
        
        
        return apps
    
    def get_suggestions_v2(self,keyword):
        url = f'https://m.apkpure.com/search?q={keyword}'
        
        data = []
        
        soup = None
        
        for i in range(0, self.max_retry):
            try:
                response = self.wd.get(url,proxies=self.proxy)
                print(response.status_code)
                if response.status_code == 200:
                    try:
                        soup = BeautifulSoup(response.text)
                        break
                    except:
                        pass
            except:
                pass

        if soup == None:
            return False, data
        
        for app in self.extract_suggestions_v2(soup):
            data.append(app)
        return True,data
    
    def scrape_app_details(self, url):
        soup = None
        data = {}

        for i in range(0, self.max_retry):
            response = self.wd.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text)
                break

        if soup == None:
            return False, data

        title = soup.find("div", {"class": "title-like"}).text.strip()

        download_btn = soup.find("div", {"id": "down_btns"})

        download_page_url = self.base_url + download_btn.find("a").get("href")

        apk_version = download_btn.get("data-dt-version")

        version_code = download_btn.get("data-dt-versioncode")

        apk_size_bytes = download_btn.get("data-dt-filesize")

        apk_size_text = soup.find("span", {"class": "fsize"}).find("span").text

        published_on_text = soup.find(
            "p", {"itemprop": "datePublished"}).text.strip()

        minimum_requirements = soup.find(
            "strong", string="Requirements:").parent.parent.text.replace("Requirements:", "").strip()

        data["title"] = title

        data["version"] = apk_version

        data["version_code"] = version_code

        data["size_bytes"] = apk_size_bytes

        data["size_text"] = apk_size_text

        data["published_on_text"] = published_on_text

        data["published_on_timestamp"] = string_to_datetime(published_on_text)

        data["minimum_requirements"] = minimum_requirements

        data["download_page_url"] = download_page_url

        return True, data

    def download_apk(self, url):

        soup = None
        for i in range(0, self.max_retry):

            response = self.wd.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text)
                break

        if soup == None:
            return False, None, None

        download_link = soup.find("a", {"id": "download_link"}).get("href")

        file_bytes = None

        for i in range(0, self.max_retry):
            response = self.wd.get(download_link)
            if response.status_code == 200:
                file_bytes = response.content
                break

        if file_bytes == None:
            return False, None, None

        return True, file_bytes, download_link


if __name__ == "__main__":
    scraper = ApkpureScraper()

    # print(scraper.get_suggestions_v2("nomao camera"))
    # for i in scraper.get_suggestions("what"):
    #     print(i)

    # data = scraper.scrape_app_details("https://apkpure.com/facebook/com.facebook.katana")
    # print(data)

    # url = "https://apkpure.com/facebook/com.facebook.katana/download?from=details"

    # status,content = scraper.download_apk(url)

    # with open("test.apk","wb") as f:
    #     f.write(content)

    # https://download.apkpure.com/b/APK/Y29tLmZhY2Vib29rLmthdGFuYV8zMTQyMTQ0NTlfMWUyZjQ1MTU?_fn=RmFjZWJvb2tfdjM3MS4wLjAuMjQuMTA5X2Fwa3B1cmUuY29tLmFwaw&as=b9bb962ee431d4939163cda4ccd292ec62b49354&ai=1803426660&at=1656001244&_sa=ai%2Cat&k=26690eb5bf7af4b7f310a451cd175a9562b735dc&r=https%3A%2F%2Fapkpure.com%2Ffacebook%2Fcom.facebook.katana&_p=Y29tLmZhY2Vib29rLmthdGFuYQ&c=1%7CSOCIAL%7CZGV2PU1ldGElMjBQbGF0Zm9ybXMlMkMlMjBJbmMuJnQ9YXBrJnM9NTIzMzIxMzcmdm49MzcxLjAuMC4yNC4xMDkmdmM9MzE0MjE0NDU5&hot=1
