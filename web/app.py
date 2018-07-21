from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.SentencesDatabase
users = db["Users"]

class Register(Resource):
    def post(self):
        posted_data = request.get_json()

        # TODO: check posted_data incoming data
        username = posted_data["username"]
        password = posted_data["password"]

        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        # TODO: Check for duplicate username

        users.insert({
            "username": username,
            "password": hashed_pw,
            "Sentence": "",
            "Tokens": 10
        })

        resp = {
            "status": 200,
            "Message": "Successfully signed up for API"
        }

        return jsonify(resp)

def verifyPw(username, pw):
     hashed_pw = users.find(
         {"username": username}
     )[0]["password"]

     if bcrypt.hashpw(pw.encode('utf8'), hashed_pw.encode('utf8')) == hashed_pw:
         return True
     else:
         return False

def countTokens(username):
    return users.find({"username": username})[0]["Tokens"]

class Store(Resource):
    def post(self):
        posted_data = request.get_json()

        # TODO: check posted_data incoming data
        username = posted_data["username"]
        password = posted_data["password"]
        sentence = posted_data["sentence"]

        correct_pw = verifyPw(username, password)

        if not correct_pw:
            resp = {
                "status": 302
            }
            return jsonify(resp)
        
        num_of_tokens = countTokens(username)

        if num_of_tokens <= 0:
            resp = {
                "status": 301
            }
            return jsonify(resp)

        users.update(
            {
                "username": username
            },
            {
                "$set": {
                    "Sentence": sentence,
                    "Tokens": num_of_tokens - 1
                }
            }
        )

        resp = {
            "status": 200,
            "Message": "Successfully added sentence"
        }

        return jsonify(resp)

class Get(Resource):
    def post(self):
        posted_data = request.get_json()

        # TODO: check posted_data incoming data
        username = posted_data["username"]
        password = posted_data["password"]

        correct_pw = verifyPw(username, password)

        if not correct_pw:
            resp = {
                "status": 302
            }
            return jsonify(resp)
        
        num_of_tokens = countTokens(username)

        if num_of_tokens <= 0:
            resp = {
                "status": 301
            }
            return jsonify(resp)

        sentence = users.find({
            "username": username
        })[0]["Sentence"]

        users.update(
            {
                "username": username
            },
            {
                "$set": {
                    "Tokens": num_of_tokens - 1
                }
            }
        )
        
        resp = {
            "status": 200,
            "Sentence": sentence
        }

        return jsonify(resp)


api.add_resource(Register ,"/register")
api.add_resource(Store, "/store")
api.add_resource(Get, "/get")

@app.route('/')
def hello_world():
    return "Hello World!"

if __name__ == "__main__":
    app.run(host="0.0.0.0")
