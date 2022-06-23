from bs4 import BeautifulSoup
import cloudscraper

scraper = cloudscraper.create_scraper()

url = "https://apkpure.com/whatsapp-messenger/com.whatsapp/download?from=details"

response = scraper.get(url)

soup = BeautifulSoup(response.text)

download_link = soup.find("a",{"id":"download_link"}).get("href")

print(download_link)