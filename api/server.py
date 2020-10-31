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

class player:
    def __init__(self,uid, uname, passwd, currenthealth, currentbalance, currentplayerdamage,damagemodifier):
        self.uid = uid
        self.uname = uname
        self.password = passwd
        self.currenthealth = currenthealth
        self.currentbalance = currentbalance
        self.currentplayerdamage = currentplayerdamage
        self.damagemodifier = damagemodifier
        self.currentbosshealth = 50
        self.inventory = []
        self.currentlyepquippedweapon = ''

    
  
class boss:
    def __init__(self,health,damage,type,imgpath,frames):
        self.health = health
        self.damage = damage
        self.type = "pumpkin"
        self.imgpath = imgpath
        self.frames = frames

# class boss:

#     def __init__(self,currentbosshealth, currentbossdamage):
#         self.currentbossdamage = currentbossdamage
#         self.currentbosshealth = currentbosshealth
     


# db.add_user("123@test.com","josh",x.password.decode("utf-8"))

user = json.loads(db.get_user("123@test.com"))
uid = user['id']
uname = user['username']
passwd = user['password']
dam = user["curdmg"]
currentbal = user["curbalance"]

x = player(uid, uname, passwd,100,currentbal,dam, 10)
b = boss(50,50,"pumpkin","imgpath","frames")

    # b = boss(2000,20)
    
user_inventory = json.loads(db.get_userinventory("123@test.com"))
iteminfo = json.loads(db.get_item('water cooling'))
print(user_inventory)
    # db.give_money("123@test.com", 9999999)
(db.buy_item("123@test.com", 'melting laser'))
   
if (user_inventory["meltinglaser"]):
    print("hello")


print(x.currentplayerdamage + iteminfo["dmginc"])






#player functions

@app.route('/login', methods=['POST']) 
def login():
    data = request.json
    email = data["email"]
    user = json.loads(db.get_user(email))
    password = data["password"]

    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(passwd, salt)
    hashpass = hashed
    if (hashpass == user["password"]):
        return "passwords match", 201
    else:
        return "passwords do not match",201

    

@app.route('/updateplayerdamage', methods=['POST']) 
def updateplayerdamage():
    data = request.json
    newplayerdamage = x.currentplayerdamage + data["damagemodifier"]
    x.currentplayerdamage = newplayerdamage
    return jsonify({"newplayerdamage" : newplayerdamage }), 201

@app.route('/getplayerdamage', methods=['POST']) 
def getplayerdamage():
    return jsonify({"currentplayerdamage" : x.currentplayerdamage }), 201

@app.route('/updateplayerbalance', methods=['POST']) 
def updateplayerbalance():
    data = request.json
    newplayerbalance = x.currentbalance + data["playerbalancemodifier"]
    x.currentbalance = newplayerbalance
    return jsonify({"currentplayerbalance" : newplayerbalance }), 201

@app.route('/getplayerbalance', methods=['POST']) 
def getplayerbalance():
    return jsonify({"currentplayerbalance" : x.currentbalance }), 201

@app.route('/getplayerinventory', methods=['POST']) 
def getplayerinventory():
    return jsonify(x.inventory), 201

@app.route('/addtoplayerinventory', methods=['POST']) 
def addtoplayerinventory():
    data = request.json
    x.inventory.append(data)
    return jsonify(x.inventory), 201

@app.route('/buyitem', methods=['POST']) 
def buyitem():
    data = request.json
    itemname = data['itemname']
    (db.buy_item("123@test.com", itemname))
    return "item was purchased", 201

@app.route('/consume', methods=['POST']) 
def consume():
    data = request.json
    consumable_name = data['consumable_name']
    email = data['email']
    json.loads(db.consume(email, consumable_name))
    return "item was consumed", 201
# @app.route('/setequippedweapon', methods=['POST']) 
# def buyitem():
#     data = request.json
#     weaponname = data['weaponname']
#     (db.buy_item("123@test.com", itemname))
#     return "item was purchased", 201

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
    iteminfo = json.loads(db.get_item(data['itemname']))
    totaldamage = user["curdmg"] + iteminfo["dmginc"]
    b.health = b.health - totaldamage
    return jsonify({"currentbosshealth" : b.health }), 201

@app.route('/getbosshealth', methods=['POST']) 
def getbosshealth():
    return jsonify({"currentbosshealth" : b.currentbosshealth }), 201

# @app.route('/updatebossdamage', methods=['POST']) 
# def updatebossdamage():
#     data = request.json
#     newbossdamage =  50 + data["currentbossdamagemodifier"]
#     b.currentbossdamage = newbossdamage
#     return jsonify({"currentbossdamage" : b.currentbossdamage }), 201

@app.route('/getbossdamage', methods=['POST']) 
def getbossdamage():
    return jsonify({"currentbossdamage" : b.currentbossdamage }), 201




if __name__ == '__main__':
    app.run(port=8080)