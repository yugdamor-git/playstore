from flask import Flask, Response, jsonify, redirect, request,send_from_directory
from database import Database
from flask_cors import CORS

from pathlib import Path
import shutil
from apkpure_scraper import ApkpureScraper
from ttl_token import TllToken


app = Flask(__name__)

CORS(app)

db = Database()

token_generator = TllToken()

scraper = ApkpureScraper()

# to get search suggestion from keyword
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

@app.route('/delete-application',methods=["GET"])
def delete_application():
    package_id = request.args.get("package_id")
    
    status,message = db.delete_application(package_id)
    
    return jsonify({
        "status":status,
        "message":message
    })

@app.route('/update-application',methods=["POST"])
def update_application():
    package_id = request.args.get("package_id")
    
    data = request.json["data"]
    
    db.update_application(package_id,data)
    
    return jsonify({
        "status":True,
        "message":"data updated"
    }),200
    
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