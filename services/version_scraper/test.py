url = "https://apkpure.com/facebook/com.facebook.katana"

from playwright_driver import PlaywrightDriver
wd = PlaywrightDriver()

wd.start()

wd.page.goto(url)
soup = wd.get_soup()

title = soup.find("div",{"class":"title-like"}).text.strip()

download_btn = soup.find("div",{"class":"down_btns"})

apk_version = download_btn.get("data-dt-version")
version_code = download_btn.get("data-dt-versioncode")
apk_size = download_btn.get("data-dt-filesize")

published_on = soup.find("p",{"itemprop":"datePublished"}).text.strip()

requirements = soup.find("strong",string="Requirements:").parent.text.replace("Requirements:","").strip()






wd.stop()

