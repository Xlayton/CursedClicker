from flask import Flask, jsonify, make_response, request, abort
import bcrypt

app = Flask(__name__)



class player:

    def __init__(self,uid, uname, passwd, currenthealth, currentbalance, currentplayerdamage,damagemodifier):
        self.uid = uid
        self.uname = uname
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(passwd, salt)
        hashpass = hashed
        self.password = hashpass
        self.currenthealth = currenthealth
        self.currentbalance = currentbalance
        self.currentplayerdamage = currentplayerdamage
        self.damagemodifier = damagemodifier
        self.currentbosshealth = 50
        self.inventory = []
        self.currentlyepquippedweapon = ''

    
  


class boss:

    def __init__(self,currentbosshealth, currentbossdamage, type):
        self.currentbossdamage = currentbossdamage
        self.currentbosshealth = currentbosshealth
        self.type = 'pumpkin'

    
x = player(00,'bob',b'bbqbob',1000,2000,10,5)
b = boss(2000,20,'pumpkin')

    


#player functions
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



#boss functions
@app.route('/updatebosshealth', methods=['POST']) 
def updatebosshealth():
    data = request.json
    newbosshealth =  b.currentbosshealth + data["currentbosshealthmodifier"]
    b.currentbosshealth = newbosshealth
    return jsonify({"currentbosshealth" : newbosshealth }), 201

@app.route('/getbosshealth', methods=['POST']) 
def getbosshealth():
    return jsonify({"currentbosshealth" : b.currentbosshealth }), 201

@app.route('/updatebossdamage', methods=['POST']) 
def updatebossdamage():
    data = request.json
    newbossdamage =  b.currentbossdamage + data["currentbossdamagemodifier"]
    b.currentbossdamage = newbossdamage
    return jsonify({"currentbossdamage" : b.currentbossdamage }), 201

@app.route('/getbossdamage', methods=['POST']) 
def getbossdamage():
    return jsonify({"currentbossdamage" : b.currentbossdamage }), 201




if __name__ == '__main__':
    app.run(port=8080)