from flask import Flask, Response, jsonify, redirect, request,send_from_directory
from database import Database
from flask_cors import CORS

from pathlib import Path
import shutil
from apkpure_scraper import ApkpureScraper
from ttl_token import TllToken
from datetime import datetime,timedelta


import json

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
    JWTManager,
)

from bson.objectid import ObjectId
from flask_bcrypt import Bcrypt

class JSONEncoder(json.JSONEncoder):
    ''' extend json-encoder class'''

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, set):
            return list(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)

app = Flask(__name__)

CORS(app)

app.config["JWT_SECRET_KEY"] = "3bc27a33-ac7d-4f15-be44-2748de7c9d57"

app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=365*100)

jwt = JWTManager(app)

flask_bcrypt = Bcrypt(app)
app.json_encoder = JSONEncoder


@jwt.unauthorized_loader
def unauthorized_response(callback):
    return redirect("/login",302)

db = Database()

token_generator = TllToken()

scraper = ApkpureScraper()


@app.route('/auth', methods=['POST'])
def auth_user():
    ''' auth endpoint '''
    
    data = request.get_json()["data"]
    
    user = list(db.users.find({'email': data['email']}))
    
    if len(user) == 0:
        return jsonify({
            "status":False,
            "message":"the email address is invalid.",
            "data":None
        })
    
    
    pwd = user[0].get("password")
    
    if user and flask_bcrypt.check_password_hash(pwd, data['password']):
        del user['password']
        del data['password']
        access_token = create_access_token(identity=data)
        refresh_token = create_refresh_token(identity=data)
        user['token'] = access_token
        user['refresh'] = refresh_token
        return jsonify({'status': True, 'data': user}), 200
    else:
        return jsonify({'status': False, 'message': 'invalid password'}), 200
    
@app.route('/refresh', methods=['POST'])
@jwt_required()
def refresh():
    ''' refresh token endpoint '''
    current_user = get_jwt_identity()
    ret = {
        'token': create_access_token(identity=current_user)
    }
    return jsonify({'ok': True, 'data': ret}), 200


@app.route('/register', methods=['POST'])
#@jwt_required()
def register():
    ''' register user endpoint '''
    
    data = request.get_json()["data"]
    
    user = list(db.users.find({'email': data['email']}))
    
    if len(user) != 0:
        return jsonify({
            "status":False,
            "message":"user already exists.",
            "data":None
        })
    
   
    data['password'] = flask_bcrypt.generate_password_hash(data['password'])
    
    db.users.insert_one(data)
    
    return jsonify({'status': True, 'msg': 'User created successfully!'}), 200


# to get search suggestion from keyword
@jwt_required()
@app.route('/get-suggestion')
def get_suggestion():
    keyword = request.args.get("q")
    
    status,data = scraper.get_suggestions(keyword)
    
    return jsonify({
        "data":data,
        "status":status
    })

# add application in database



@app.route('/add-application',methods=["POST"])
@jwt_required()
def add_application():
    data = request.json["data"]
    
    status,id,message = db.add_application(data)
    
    return jsonify({
        "status":status,
        "message":message,
        "data":{
            "_id":id
        }
    })

@app.route('/icon/<id>',methods=["GET"])
def fetch_icon(id):
    return send_from_directory(f'/downloads/{id}',"icon.png")

@jwt_required()
@app.route('/search-applications',methods=["GET"])
def search_applications():
    default_limit = 20
    limit = request.args.get("limit")
    if limit != None:
        default_limit = int(limit)
        
    keyword = request.args.get("keyword")
    
    data = db.search_applications(keyword,default_limit)
    
    return jsonify({
        "status":True,
        "message":"",
        "data":data
    })

@jwt_required()
@app.route('/delete-application',methods=["GET"])
def delete_application():
    package_id = request.args.get("package_id")
    
    status,message = db.delete_application(package_id)
    
    return jsonify({
        "status":status,
        "message":message
    })

@jwt_required()
@app.route('/update-application',methods=["POST"])
def update_application():
    package_id = request.args.get("package_id")
    
    data = request.json["data"]
    
    db.update_application(package_id,data)
    
    return jsonify({
        "status":True,
        "message":"data updated"
    }),200

@jwt_required()
@app.route('/get-recent-application',methods=["GET"])
def get_recent_application():
    default_limit = 20
    
    limit = request.args.get("limit")
    
    if limit != None:
        default_limit = int(limit)
    
    recent_application = db.get_recent_application(default_limit)
    
    return jsonify({
        "status":True,
        "data":recent_application
    }),200

@jwt_required()
@app.route('/get-application-details',methods=["GET"])
def get_application_details():
    package_id = request.args.get("package_id")
    
    status,app_details = db.get_application_details(package_id)
    
    for file in app_details["files"]:
        data = {
            "download_filename":file["filename"] + ".apk",
            "folder_name":package_id,
            "server_file_name":file["version_unique_id"] + ".apk"
        }
        
        token = token_generator.generate_ttl_token(data)
        
        file["download_token"] = token
    
    
    return jsonify({
        "status":status,
        "data":app_details
    }),200


@app.route('/download/<token>')
def download_file(token):
    
    data = token_generator.decode_ttl_token(token)
    
    download_filename = data["download_filename"]
    folder_name = data["folder_name"]
    server_file_name = data["server_file_name"]
    
    if data["status"] == True:
        return send_from_directory(f'/downloads/{folder_name}',server_file_name, as_attachment=True,download_name=download_filename)
    else:
        return redirect("https://latestmodapks.com",code=302)
    

if __name__ == '__main__':
    app.run(debug=True)