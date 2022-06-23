import json

from bs4 import BeautifulSoup


class SuggestionScraper:
    
    def __init__(self,page) -> None:
        
        self.page = page
        # self.driver = PlaywrightDriver()
        
        self.url = "https://m.apkpure.com/api/v1/search_suggestion_new?key="
        
    
    def get_soup(self):
        try:
            soup = BeautifulSoup(self.page.content(),features="html.parser")
            return soup
        except Exception as e:
            print(f'error : {str(e)}')
            return None
    
    
    def suggest(self,keyword):
        data = []
        
        # self.driver.start()
        
        try:
            url = self.url + str(keyword)
            self.page.goto(url)
            
            soup = self.get_soup()
            
            tmp = json.loads(soup.find("body").text)
            
            for item in tmp:
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
            
        except Exception as e:
            print(f'error : {str(e)}')
        
        # self.driver.stop()
        return data


# if __name__ == "__main__":
#     ss = SuggestionScraper()
#     keyword = "whatsapp"
#     for i in ss.suggest(keyword):
#         print(i)