from flask import Flask, jsonify, make_response, request, abort
import bcrypt





app = Flask(__name__)


uid = ''
passwd = b's$cret12'
uname = 'bob'
salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(passwd, salt)
hashpass = hashed
currentdamage = '100'
adddamage = '10'
currenthealth = '10000000'
currentbalance = 'x'


data = [{
    "user" : [{
    "name": "bob"
    }]
}]

# userdata = jsonify[{
#     "user" : [{
#     "uid": uid,
#     "username": uname,
#     "currentdamage" : currentdamage,
#     "currentbalance": currentbalance,
#     "damagemodifier": 10
#     }]
# }]
# bossdata = jsonify[{
#     "boss" : [{
#     "uid" : uid,
#     "type": "pumpkin",
#     "currentdamage": currentdamage,
#     "currentbosshealth" : currentbosshealth,
#     "damagemodifier": damagemodifier
#     }]
# }]


@app.route('/getuserdata', methods=['POST']) 
def create_task():

 
   
    userdata = jsonify({
    "user" : [{
    "uname": uname,
    "uid" : uid,
    "currentdamage" : currentdamage,
    "currentbosshealth": 100,
    "currentbalance": currentbalance

    }]
})
    user = request.json
    data.append(user)
    return userdata, 201

# @app.route('/updateplayerdamage', methods=['POST']) 
# def create_task():

   
#     userdata = jsonify({
#     "user" : [{
#     "uid" : uid,
#     "currentdamage" : currentdamage,
#     "currenthealth": currenthealth,
#     "currentbalance": currentbalance,
#     "damagemodifier": damagemodifier
#     }]
# })
#     user = request.json
#     userdata["currenthealth"] = userdata["currenthealth"] + userdata["damagemodifier"]
#     print(userdata[currenthealth])
#     return userdata, 201





@app.route("/data", methods=["GET"])
def getData():
    return jsonify(data)

if __name__ == '__main__':
    app.run(port=8080)