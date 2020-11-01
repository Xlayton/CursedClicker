from flask import Flask, jsonify, make_response, request, abort, Response
import bcrypt
import db
import json
import asyncio
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

#for creating a user
#  salt = bcrypt.gensalt()
#         hashed = bcrypt.hashpw(passwd, salt)
#         hashpass = hashed


# print(x.currentplayerdamage + iteminfo["dmginc"])





#player functions
@app.route('/register', methods=['POST']) 
def register():
    data = request.json
    email = data["email"]
    salt = bcrypt.gensalt()
    passwd = data["password"]
    uname = data["uname"]
    hashed = bcrypt.hashpw(str.encode(passwd), salt)
    hashpass = hashed
    ipadd = request.remote_addr
    db.add_user(email,uname,hashpass.decode("utf-8"))
    resp = Response("user registered", 201)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
   

@app.route('/getmykey', methods=['POST'])
def get_key():
    data = request.json
    email = data["email"]
    ipaddress = request.remote_addr
    resp = Response(db.get_api_key(email), 201)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
   

@app.route('/login', methods=['POST']) 
def login():
    data = request.json
    email = data["email"]
    print(email)
    print(db.get_user(email))
    user = json.loads(db.get_user(email))
    password = data["password"]

    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(str.encode(password), salt)
    hashpass = hashed
    print(hashpass)
    print(user["password"])
    print(hashpass)
    if bcrypt.checkpw(password.encode("utf-8"), user["password"].encode("utf-8")):
       
        uid = user['id']
        uname = user['username']
        passwd = user['password']
        dam = user["curdmg"]
        currentbal = user["curbalance"]
        # x = player(uid, uname, passwd,100,currentbal,dam, 10)
        
        resp = Response(db.get_user(email), 201)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    else:
        return "passwords do not match",400

    
# we dont need this one because the way to update this is through better items
# @app.route('/updateplayerdamage', methods=['POST']) 
# def updateplayerdamage():
#     data = request.json
#     email = data["email"]
#     user = json.loads(db.get_user(email))
#     newplayerdamage = user["curdmg"] + data["damagemodifier"]
#     user["curdmg"] = newplayerdamage
#     return jsonify({"newplayerdamage" : user["curdmg"] }), 201

@app.route('/getplayerdamage', methods=['POST']) 
def getplayerdamage():
    data = request.json
    api_key = data["key"]
    valid = db.confirm_key(api_key)
    
    if (valid) :
        email = data["email"]
        user = json.loads(db.get_user(email))
        resp = Response( jsonify({"currentplayerdamage" : user["curdmg"] }), 201)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
        
    else :
        resp = Response(jsonify({"message" : "no key provided"}), 400)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
       

@app.route('/updateplayerbalance', methods=['POST']) 
def updateplayerbalance():
    data = request.json
    email = data["email"]
    amount = data["amount"]
    api_key = data["key"]
    valid = db.confirm_key(api_key)
    if (valid) :
        db.give_money(email,amount, api_key)
        user = json.loads(db.get_user(email))
        return jsonify({"currentplayerbalance" : user["curbalance"] }), 201
    else :
        return jsonify({"message" : "no key provided"}), 400

@app.route('/getplayerbalance', methods=['POST']) 
def getplayerbalance():
    data = request.json
    api_key = data["key"]
    valid = db.confirm_key(api_key)
    if (valid) :
        email = data["email"]
        user = json.loads(db.get_user(email))
        return jsonify({"currentplayerbalance" : user["curbalance"] }), 201
    else :
        return jsonify({"message" : "no key provided"}), 400

@app.route('/getplayerinventory', methods=['POST']) 
def getplayerinventory():
    data = request.json
    api_key = data["key"]
    email = data["email"]
    valid = db.confirm_key(api_key)
    a = json.loads(db.get_userinventory(email,api_key))
    if (valid) :
        return a, 201
    else :  
        return jsonify({"message" : "no key provided"}), 400

@app.route('/buyconsumable', methods=['POST']) 
def buyconsumable():
    data = request.json
    api_key = data["key"]
    valid = db.confirm_key(api_key)
    if (valid) :
        email = data['email']
        item_name = data['itemname']
        db.buy_consumable(email, item_name, api_key)
        user = json.loads(db.get_user(email))
        user.inventory.append(data)
        return jsonify(user.inventory), 201
    else :
        return jsonify({"message" : "no key provided"}), 400

@app.route('/buyitem', methods=['POST']) 
def buyitem():
    data = request.json
    api_key = data["key"]
    valid = db.confirm_key(api_key)
    if (valid) :
        data = request.json
        email = data['email']
        itemname = data['itemname']
        email = data['email']
        (db.buy_item(email, itemname, api_key))
        return jsonify({"item was purchased": "success"}), 201
    else :
        return jsonify({"message" : "no key provided"}), 400



@app.route('/consume', methods=['POST']) 
def consume():
    data = request.json
    api_key = data["key"]
    valid = db.confirm_key(api_key)
    if (valid) :
        consumable_name = data['consumable_name']
        email = data['email']
        json.loads(db.consume(email, consumable_name, api_key))
        return "item was consumed", 201
    else :
        return jsonify({"message" : "no key provided"}), 400

#boss functions
@app.route('/updatebosshealth', methods=['POST']) 
def updatebosshealth():
    data = request.json
    api_key = data["key"]
    bn = data["bossname"]
    valid = db.confirm_key(api_key)
    if (valid) :
        bosshealth = json.loads(db.get_boss_health(bn))
        newbosshealth =  bosshealth+ data["currentbosshealthmodifier"]
        bosshealth = newbosshealth
        db.set_boss_health(bn,bosshealth)
        return jsonify({"currentbosshealth" : newbosshealth }), 201
    else :
        return jsonify({"message" : "no key provided"}), 400

@app.route('/attacktheboss', methods=['POST']) 
def attacktheboss():
    data = request.json
    api_key = data["key"]
    valid = db.confirm_key(api_key)
    if (valid) :
        useremail = data["email"]
        user_inventory = json.loads(db.get_userinventory(useremail, api_key))
        user = json.loads(db.get_user(useremail))
        bn = data['boss_name']
        bosshealth = json.loads(db.get_boss_health(bn))
        iteminfo = json.loads(db.get_item(data['itemname']))
        totaldamage = user["curdmg"] + iteminfo["dmginc"]
        bosshealth = bosshealth - totaldamage
        db.set_boss_health(bn,bosshealth, api_key)
        return jsonify({"currentbosshealth" : bosshealth }), 201
    else :
        return jsonify({"message" : "no key provided"}), 400

@app.route('/getbosshealth', methods=['POST']) 
def getbosshealth():
    data = request.json
    api_key = data["key"]
    valid = db.confirm_key(api_key)
    if (valid) :
        bn = data['boss_name']
        bosshealth = json.loads(db.get_boss_health(bn))
        return jsonify({"currentbosshealth" : bosshealth }), 201
    else :
        return jsonify({"message" : "no key provided"}), 400

# @app.route('/updatebossdamage', methods=['POST']) 
# def updatebossdamage():
#     data = request.json
#     newbossdamage =  50 + data["currentbossdamagemodifier"]
#     b.currentbossdamage = newbossdamage
#     return jsonify({"currentbossdamage" : b.currentbossdamage }), 201






if __name__ == '__main__':
    app.run(port=8080)