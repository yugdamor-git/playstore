import cloudscraper

scraper = cloudscraper.create_scraper()

response = scraper.get("https://download.apkpure.com/b/APK/Y29tLmluc3RhZ3JhbS5hbmRyb2lkXzM2NDAwNDg2Ml8zZjgyMmVlOQ?_fn=SW5zdGFncmFtX3YyNDAuMi4wLjE4LjEwN19hcGtwdXJlLmNvbS5hcGs&as=0461bcc152048dccfe7a4534254aff7162b41fb4&ai=-1067878840&at=1655971644&_sa=ai%2Cat&k=9f3b28239884fe8b2296a46dc985416862b6c23c&_p=Y29tLmluc3RhZ3JhbS5hbmRyb2lk&c=1%7CSOCIAL%7CZGV2PUluc3RhZ3JhbSZ0PWFwayZzPTUyMjEzODk3JnZuPTI0MC4yLjAuMTguMTA3JnZjPTM2NDAwNDg2Mg")

with open("test.apk","wb") as f:
    f.write(response.content)