from gevent import monkey
monkey.patch_all()


from helper import clean_package_name

from flask import Flask, jsonify, redirect, request,send_from_directory
from suggestion_scraper import SuggestionScraper
import os
from database import Database
from custom_playwright_driver import PlaywrightDriver
from schemas import package_schema,app_schema
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError
from flask_cors import CORS

from json_encoder import JSONEncoder

def validate_payload(data,schema):
    try:
        validate(data, schema)
    except ValidationError as e:
        return {'ok': False, 'msg': e}
    except SchemaError as e:
        return {'ok': False, 'msg': e}
    return {'ok': True, 'data': data}

app = Flask(__name__)
CORS(app)
# app.config["MONGO_URI"] = f'mongodb://{user}:{password}@{host}/{database}?authSource=admin'
# app.config["MONGO_URI"] = f'mongodb://{host}/{database}?authSource=admin'

driver = PlaywrightDriver()
db = Database()

user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"



@app.route('/test-redirect')
def test_redirect():
    url= "https://download.apkpure.com/b/APK/Y29tLmluc3RhZ3JhbS5hbmRyb2lkXzM2MzUwNDk4NF82OGFmYzkxMQ?_fn=SW5zdGFncmFtX3YyMzUuMC4wLjIxLjEwN19hcGtwdXJlLmNvbS5hcGs&as=b9e2c9351cb7977aadc5bd16fbae893962b42052&ai=298936170&at=1655971802&_sa=ai%2Cat&k=594dc0db6cbca2a9dd5aa36653de967a62b6c2da&_p=Y29tLmluc3RhZ3JhbS5hbmRyb2lk&c=1%7CSOCIAL%7CZGV2PUluc3RhZ3JhbSZ0PWFwayZzPTU5NDQ2MjY2JnZuPTIzNS4wLjAuMjEuMTA3JnZjPTM2MzUwNDk4NA"
    return redirect(url,code=302) 

@app.route('/suggest')
def suggestion():
    keyword = request.args.get("q")
    
    browser = driver.browser.new_context(user_agent=user_agent)
    
    page = browser.new_page()
    
    ss = SuggestionScraper(page)
    
    data = ss.suggest(keyword)
    
    page.close()
    
    return jsonify(data)


@app.route('/update-app',methods=["POST"])
def update_app():
    data = validate_payload(request.get_json(),package_schema)
    if data['ok']:
        
        req_data = data["data"]["data"]
        
        id = data["data"]["id"]
        
        db.update_app(id,req_data)
        
        return jsonify({'ok':True,"message":"data is updated. you can reload the page now."})
        
    else:
        return jsonify({'ok': False,'data':None, 'message': 'Bad request parameters: {}'.format(data['msg'])}), 400


@app.route('/media/<folderName>/<fileName>')
def download_file(folderName,fileName):
    apk_data = list(db.apk.find({"apk_unique_id":fileName}))[0]
    
    ext = None
    if apk_data["type"] == "APK" or apk_data["type"] == "apk":
        ext = "apk"
    else:
        ext = "zip"
        
    file_name = f'{fileName}.{ext}'
    return send_from_directory(f'/downloads/{folderName}',file_name, as_attachment=True,download_name=f'{apk_data["apk_id"]}.{ext}')

@app.route('/delete-app',methods=["GET"])
def delete_app():
    
    package_id = request.args.get("package_id")
    
    db.delete_app(package_id)
    
    return jsonify({'ok': True,"message":"app deleted."}), 200

@app.route('/add-app',methods=["POST"])
def add_app():
    data = validate_payload(request.get_json(),package_schema)
    if data['ok']:
        package_name = data["data"]["package_name"]
        req_data = data["data"]["data"]
        
        package_name = clean_package_name(package_name)
        
        data = db.get_app_by_package_name(package_name)
        
        if len(data) > 0:
            return jsonify({'ok':False,"message":"we already have this app in our database."}),200
        else:
            id = db.add_app(req_data)
            
            return jsonify({'ok': True,"message":f'{req_data["title"]} is added.'}), 200
        
    else:
        return jsonify({'ok': False,'data':None, 'message': 'Bad request parameters: {}'.format(data['msg'])}), 400

@app.route('/get-recent-apps',methods=["GET"])
def add_recent_apps():
    default_limit = 20
    
    limit = request.args.get("limit",None)
    
    if limit != None:
        default_limit = int(limit)
    
    apps = db.get_recent_apps(default_limit)
    
    return jsonify({'ok':True,"data":apps})
    


@app.route('/search-apps',methods=["GET"])
def search_apps():
    default_limit = 5
    
    limit = request.args.get("limit",None)
    
    keyword = request.args.get("q","")
    
    
    if limit != None:
        default_limit = int(limit)
    
    
    apps = db.find_app(keyword,default_limit)
    
    return jsonify({'ok':True,"data":apps})

@app.route('/get-app-details',methods=["GET"])
def get_app_details():
    
    id = request.args.get("id")
    
    app = db.get_app_details_by_id(id)
    
    return jsonify({'ok':True,"data":app})

@app.route('/package',methods=["GET"])
def package_get():
    data = validate_payload(request.get_json(),package_schema)
    if data['ok']:
        data = data["data"]
        
        package_name = clean_package_name(data["package_name"])
        
        data = db.get_package(package_name)
        
        return jsonify({'ok': True,'data':data}), 200
        
    else:
        return jsonify({'ok': False,'data':None, 'message': 'Bad request parameters: {}'.format(data['msg'])}), 400
    


    
@app.route('/package/update',methods=["POST"])
def package_post():
    data = validate_payload(request.get_json(),package_schema)
    if data['ok']:
        data = data["data"]
        
        package_name = clean_package_name(data["package_name"])
        
        data = db.update_package(package_name,data["data"])
        
        return jsonify({'ok': True,'data':data}), 200
        
    else:
        return jsonify({'ok': False,'data':None, 'message': 'Bad request parameters: {}'.format(data['msg'])}), 400
    


@app.route('/package/create',methods=["POST"])
def package_post_create():
    data = validate_payload(request.get_json(),package_schema)
    if data['ok']:
        data = data["data"]
        
        package_name = clean_package_name(data["package_name"])
        
        data = db.insert_package(package_name,data["data"])
        
        return jsonify({'ok': True,'data':data}), 200
        
    else:
        return jsonify({'ok': False,'data':None, 'message': 'Bad request parameters: {}'.format(data['msg'])}), 400


@app.route('/app',methods=["GET"])

def app_get():
    data = validate_payload(request.get_json(),app_schema)
    if data['ok']:
        data = data["data"]
        
        app_id = data["app_id"]
        
        data = db.get_app(app_id)
        
        return jsonify({'ok': True,'data':data}), 200
        
    else:
        return jsonify({'ok': False,'data':None, 'message': 'Bad request parameters: {}'.format(data['msg'])}), 400
    
@app.route('/app',methods=["POST"])
def app_post():
    data = validate_payload(request.get_json(),app_schema)
    if data['ok']:
        data = data["data"]
        
        app_id = data["app_id"]
        
        data = db.update_app(app_id,data["data"])
        
        return jsonify({'ok': True,'data':data}), 200
        
    else:
        return jsonify({'ok': False,'data':None, 'message': 'Bad request parameters: {}'.format(data['msg'])}), 400


@app.route('/package',methods=["DELETE"])
def package_delete():
    data = validate_payload(request.get_json(),package_schema)
    if data['ok']:
        data = data["data"]
        
        package_name = clean_package_name(data["package_name"])
        
    else:
        return jsonify({'ok': False,'data':None, 'message': 'Bad request parameters: {}'.format(data['msg'])}), 400


if __name__ == '__main__':
    app.run(debug=True)