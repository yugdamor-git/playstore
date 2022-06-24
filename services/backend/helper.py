
import hashlib
from dateutil import parser
from datetime import datetime
import requests

def string_to_datetime(text):
    try:
        date = parser.parse(text)
        return date
    except:
        return None
    
def generate_sha1_hex(text):
    
    sha1 = hashlib.sha1()
    sha1.update(str(text).lower().strip().encode("utf-8"))
    
    return str(sha1.hexdigest())

def get_current_timestamp():
    return datetime.now()

def generate_file_id(package_name,version,version_code,published_on):
    
    tmp = f'{package_name}-{version}-{version_code}-{published_on}'.lower().strip()
    
    id = generate_sha1_hex(tmp)
    
    return tmp,id

def download_image(url):
    for i in range(0,5):
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
    return None

def save_image(folder_path,file_path,content):
    if not folder_path.exists():
        folder_path.mkdir()
    
    if not file_path.exists():
        with open(file_path,"wb") as f:
            f.write(content)
    