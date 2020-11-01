from flask import Flask, jsonify, make_response, request, abort, Response, send_from_directory
import bcrypt
import db
import json
import asyncio
import sys
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
CORS(app)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["2147483647 per day", "2147483647 per hour"]
)

currentboss = {
    "name" : "Pumpkin King",
    "health" : 20000,
    "currenthealth" : 20000,
    "imgpath": "//skull/skull.gif"
}

#for creating a user
#  salt = bcrypt.gensalt()
#         hashed = bcrypt.hashpw(passwd, salt)
#         hashpass = hashed


# print(x.currentplayerdamage + iteminfo["dmginc"])

<<<<<<< Updated upstream


@app.route('/<path:filename>')
def image(filename):
    try:
        w = int(request.args['w'])
        h = int(request.args['h'])
    except (KeyError, ValueError):
        return send_from_directory('.', filename)

    try:
        im = Image.open(filename)
        im.thumbnail((w, h), Image.ANTIALIAS)
        io = StringIO.StringIO()
        im.save(io, format='JPEG')
        return Response(io.getvalue(), mimetype='image/jpeg')

    except IOError:
        abort(404)

    return send_from_directory('.', filename)

@app.route('/getcurrentboss', methods=['GET'])
def get_current_boss() :
    return jsonify(currentboss), 200

=======
>>>>>>> Stashed changes
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

@app.route('/getcooldown', methods=['POST'])      
def getcooldown():
    data = request.json
    api_key = data["key"]
    valid = db.confirm_key(api_key)
    if(valid) :
        email = data["email"]
        user = json.loads(db.get_user(email))
        uid = user['id']
        a = json.loads(db.get_userinventory(uid))
        if(a.liquidnitrogen) :
            b = json.loads(db.get_item("liquid nitrogen"))
            return b['cooldowntime']
        elif(a.watercooling) :
            b = json.loads(db.get_item("water cooling"))
            return b['cooldowntime']
        elif(a.icepack) :
            b = json.loads(db.get_item("ice pack"))
            return b['cooldowntime']

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
        userinventory = db.get_userinventory(email, api_key)
        return json.dumps(userinventory), 201
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
        db.buy_item(email, itemname, api_key)
        return json.dumps(userinventory), 201
    else :
        return jsonify({"message" : "no key provided"}), 400



@app.route('/consume', methods=['POST']) 
def consume():
    data = request.json
    api_key = data["key"]
    valid = db.confirm_key(api_key)
    if (valid) :
        consumable_name = data['itemname']
        email = data['email']        
        db.consume(email, consumable_name, api_key)
        if(consumable_name == "bomb"):
            currentboss["currenthealth"] -= 10000
        return jsonify({"name" : currentboss["name"], "health" : currentboss["health"], "currenthealth" : currentboss["currenthealth"]}), 201
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

@app.route('/getconsumables', methods=['GET'])
def get_consumables():
    resp = Response(db.get_consumables(), 200)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/getitems', methods=['GET'])
def get_items():
    resp = Response(db.get_items(), 200)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/attacktheboss', methods=['POST']) 
@limiter.limit("2147483647/second", override_defaults=True)
def attacktheboss():
    data = request.json
    api_key = data["key"]
    valid = db.confirm_key(api_key)
    if (valid) :
        useremail = data["email"]
        user_inventory = json.loads(db.get_userinventory(useremail, api_key))
        user = json.loads(db.get_user(useremail))
        itemname = ""
        if(user_inventory["pulverizinglaser"]['value'] == "True") :
            itemname = "pulverizing laser"
        elif(user_inventory["meltinglaser"]['value'] == "True") :
            itemname = "melting laser"
        elif(user_inventory["damaginglaser"]['value'] == "True") :
            itemname = "damaging laser"
        totaldamage = 0
        if(itemname != "") :
            iteminfo = json.loads(db.get_item(itemname))
            totaldamage = int(user["curdmg"] + iteminfo["dmginc"])
        else :
            totaldamage = int(user["curdmg"])
        currentboss["currenthealth"] -= totaldamage
        db.give_money(useremail, 10000, api_key)
        return jsonify({"health" : currentboss["health"], "currenthealth" : currentboss["currenthealth"], "name": currentboss["name"], "balance" : 10000}), 200
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


@app.route('/getimage', methods=['POST']) 
def getimages():
    data = request.json
    api_key = data["key"]
    valid = db.confirm_key(api_key)
    if (valid) :
        email = data['email']
        item_name = data['itemname']
        bosstype = data["bosstype"]
        if bosstype == "pumpkin":
            return jsonify({"type":"pumpkin","numberofFrames":10,"path":"pumpkin"}), 201
        elif bosstype == "skull":
            return jsonify({"type":"skull","numberofFrames":9,"path":"skull"}), 201
        elif bosstype == "candymonster":
            return jsonify({"type":"candy","numberofFrames":10,"path":"candy"}), 201
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