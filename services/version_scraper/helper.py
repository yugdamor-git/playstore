import hashlib
from dateutil import parser

def create_unique_apk_id(package_name,version,version_code,type):
    
    raw_id = f'{package_name.strip()}-{version.strip()}-{version_code.strip()}-{type.strip()}'.lower().strip()
    
    return raw_id


def find_value_by_text(element,text):
    value = None
    try:
        tmp = element.find("strong",string=text)
        
        value = tmp.parent.text.strip().replace(text,"").strip()
    except:
        pass
    return value

def string_to_datetime(text):
    try:
        date = parser.parse(text)
        return date
    except:
        return None
    
def get_apk_unique_id_from_url(url):
    tmp = url.split("?")[0].split("/")[-1]
    return tmp

def generate_unique_id(url):
    
    h = hashlib.sha1()
    
    h.update(str(url).encode("utf-8"))
    
    return str(h.hexdigest())


def extract_meta_data_from_url(url):
    unique_id = get_apk_unique_id_from_url(url)
    parts = unique_id.split("-")
    version_code = parts[0]
    apk_type = parts[1]
    unique_id = generate_unique_id(url)
    return unique_id,version_code,apk_type




# # https://apkpure.com/subway-surfers-1/com.kiloo.subwaysurf/versions

# app_id = create_unique_apk_id(
#     "com.kiloo.subwaysurf",
#     "V2.29.0",
#     "22970",
#     "APK"
    
# )

# print(app_id)