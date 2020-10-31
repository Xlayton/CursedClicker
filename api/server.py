from flask import Flask, jsonify
import bcrypt


app = Flask(__name__)


uid = ''
passwd = b's$cret12'
uname = 'bob'
salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(passwd, salt)
hashpass = hashed
currentdamage = ''


data = [
    {'name': 'Josh'},
    {'name': 'Bob'}
]


@app.route("/datapost", methods=["POST"])
def getData():
    return jsonify(data)




@app.route("/data", methods=["GET"])
def getData():
    return jsonify(data)

if __name__ == '__main__':
    app.run(port=8080)