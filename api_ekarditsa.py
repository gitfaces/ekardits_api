from flask import Flask, render_template, request
import json
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson import json_util
from flask_cors import CORS, cross_origin
import time

app = Flask(__name__)
app.config['DEBUG'] = True
cors = CORS(app)

client = MongoClient('localhost', 27017)
db = client.ekarditsa
stores = db.stores

@app.before_request
def basic_authentication():
    if request.method.lower() == 'options':
        data = {"status": "success"}
        return data, 200

@app.route('/', methods=('GET', 'POST'))
@cross_origin()
def index():
    if request.method=='POST':
        print(request.json)
        full_name=request.json['full_name']
        phone=request.json['phone']
        email=request.json['email']
        company=request.json['company']
        activity=request.json['activity']
        site=request.json['site']
        store_phone=request.json['store_phone']
        store_email=request.json['store_email']
        store_address=request.json['store_address']
        logo=request.json['logo']
        city_code=request.json['city_code']
        store_description=request.json['store_description']
        category=request.json['category']
        stores.insert_one({"active":False, "full_name":full_name,"phone":phone,"email":email,"company":company,"activity":activity,"site":site,"store_phone":store_phone,"store_email":store_email,"store_address":store_address,"city_code":city_code,"store_description":store_description, "category":category,"logo":logo, "created":time.ctime()})
        return 'ok'

    all_stores = stores.find()
    return render_template('index.html', stores=all_stores)

@app.route('/stores', methods=['POST'])
@cross_origin()
def c_stores():
    b=request.json
    q={"active":True}
    if "category" in b:
        q["category"]=b["category"]
    if "id" in b:
        q["_id"]=ObjectId(b["id"])
    category_stores = stores.find(q)
    if "sort" in b:
        category_stores.sort(b["sort"],-1)
    return json.dumps(list(category_stores), default=str)

@app.route('/test', methods=['GET'])
@cross_origin()
def test():
    return 'test'

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5002)  # run our Flask app