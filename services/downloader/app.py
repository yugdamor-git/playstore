from flask import Flask, jsonify, redirect, request,send_from_directory
from database import Database
from flask_cors import CORS

from pathlib import Path
import shutil
from apkpure_scraper import ApkpureScraper


app = Flask(__name__)
CORS(app)

db = Database()

scraper = ApkpureScraper()

# to get search suggestion from keyword
@app.route('/get-suggestion')
def get_suggestion():
    keyword = request.args.get("q")
    
    status,data = scraper.get_suggestions(keyword)
    
    return jsonify({
        "data":data,
        "status":status
    }),200

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
    }),200


@app.route('/delete-application',method=["GET"])
def delete_application():
    package_id = request.args.get("package_id")
    
    status,message = db.delete_application(package_id)
    
    return jsonify({
        "status":status,
        "message":message
    }),200

@app.route('/update-application',method=["POST"])
def update_application():
    package_id = request.args.get("package_id")
    
    data = request.json["data"]
    
    db.update_application(package_id,data)
    
    return jsonify({
        "status":True,
        "message":"data updated"
    }),200
    
@app.route('/get-recent-application',method=["GET"])
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

@app.route('/get-application-details',method=["GET"])
def get_recent_application():
    default_limit = 20
    
    package_id = request.args.get("package_id")
    
    status,app_details = db.get_application_details(package_id)
    
    return jsonify({
        "status":status,
        "data":app_details
    }),200


if __name__ == '__main__':
    app.run(debug=True)