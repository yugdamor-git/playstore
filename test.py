url = "https://download.apkpure.com/b/APK/Y29tLndoYXRzYXBwXzIyMTQxMjAwNF9jYTkxZmNhMA?_fn=V2hhdHNBcHAgTWVzc2VuZ2VyX3YyLjIyLjE0LjEyX2Fwa3B1cmUuY29tLmFwaw&as=99ca774688802c93aea34ae60d008d7b62b4ab05&ai=1803426660&at=1656007309&_sa=ai%2Cat&k=3e14cebe6c4464e0e395e2145424100b62b74d8d&_p=Y29tLndoYXRzYXBw&c=1%7CCOMMUNICATION%7CZGV2PVdoYXRzQXBwJTIwTExDJnQ9YXBrJnM9NDA5OTgzOTMmdm49Mi4yMi4xNC4xMiZ2Yz0yMjE0MTIwMDQ&hot=1"

from playwright_driver import PlaywrightDriver

driver = PlaywrightDriver()

driver.start()

with driver.page.expect_download() as download_info:
    driver.page.goto(url)
    
file = download_info.value

file.save_as("test.apk")

print(file.url)

driver.stop()