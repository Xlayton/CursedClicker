from flask import Flask, jsonify, make_response, request, abort
import bcrypt
import db
import json
import asyncio


app = Flask(__name__)

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
    db.add_user(email,uname,hashpass.decode("utf-8"))
    return "user registered", 201

@app.route('/login', methods=['POST']) 
def login():
    data = request.json
    email = data["email"]
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
        return email, 201
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
    email = data["email"]
    user = json.loads(db.get_user(email))
    return jsonify({"currentplayerdamage" : user["curdmg"] }), 201

@app.route('/updateplayerbalance', methods=['POST']) 
def updateplayerbalance():
    data = request.json
    email = data["email"]
    amount = data["amount"]
    db.give_money(email,amount)
    user = json.loads(db.get_user(email))
    return jsonify({"currentplayerbalance" : user["curbalance"] }), 201

@app.route('/getplayerbalance', methods=['POST']) 
def getplayerbalance():
    data = request.json
    email = data["email"]
    user = json.loads(db.get_user(email))
    return jsonify({"currentplayerbalance" : user["curbalance"] }), 201

@app.route('/getplayerinventory', methods=['POST']) 
def getplayerinventory():
    return jsonify(x.inventory), 201

@app.route('/buyconsumable', methods=['POST']) 
def buyconsumable():
    data = request.json
    email = data['email']
    item_name = data['itemname']
    db.buy_consumable(email, item_name)
    user = json.loads(db.get_user(email))
    user.inventory.append(data)
    return jsonify(user.inventory), 201

@app.route('/buyitem', methods=['POST']) 
def buyitem():
    data = request.json
    email = data['email']
    itemname = data['itemname']
    email = data['email']
    (db.buy_item(email, itemname))
    return "item was purchased", 201



@app.route('/consume', methods=['POST']) 
def consume():
    data = request.json
    consumable_name = data['consumable_name']
    email = data['email']
    json.loads(db.consume(email, consumable_name))
    return "item was consumed", 201



#boss functions
@app.route('/updatebosshealth', methods=['POST']) 
def updatebosshealth():
    data = request.json
    newbosshealth =  b.currentbosshealth + data["currentbosshealthmodifier"]
    b.currentbosshealth = newbosshealth
    return jsonify({"currentbosshealth" : newbosshealth }), 201

@app.route('/attacktheboss', methods=['POST']) 
def attacktheboss():
    data = request.json
    useremail = data["email"]
    user_inventory = json.loads(db.get_userinventory(useremail))
    user = json.loads(db.get_user(useremail))
    bn = data['boss_name']
    bosshealth = json.loads(db.get_boss_health(bn))
    iteminfo = json.loads(db.get_item(data['itemname']))
    totaldamage = user["curdmg"] + iteminfo["dmginc"]
    bosshealth = bosshealth - totaldamage
    db.set_boss_health(bn,bosshealth)
    return jsonify({"currentbosshealth" : bosshealth }), 201

@app.route('/getbosshealth', methods=['POST']) 
def getbosshealth():
    data = request.json
    bn = data['boss_name']
    bosshealth = json.loads(db.get_boss_health(bn))
    return jsonify({"currentbosshealth" : bosshealth }), 201

# @app.route('/updatebossdamage', methods=['POST']) 
# def updatebossdamage():
#     data = request.json
#     newbossdamage =  50 + data["currentbossdamagemodifier"]
#     b.currentbossdamage = newbossdamage
#     return jsonify({"currentbossdamage" : b.currentbossdamage }), 201






if __name__ == '__main__':
    app.run(port=8080)