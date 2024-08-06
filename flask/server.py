#!/usr/bin/env python
import os

from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongo:27017")
db = client.flask_db
users = db.flask_users

@app.route('/')
def todo():
    try:
        client.admin.command('ismaster')
    except:
        return "Server not available"
    return "Hello from the MongoDB client!\n"


@app.route('/users')
def get_user_list():
    db_users = users.find()
    list_users = [{"username": user["username"], "email": user["email"]} for user in db_users]
    return jsonify({"users": list_users})


@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data['username']
    email = data['email']

    user = {"username": username, "email": email}
    result = users.insert_one(user)

    return jsonify({"message": "User created successfully", "id": str(result.inserted_id)})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get("FLASK_SERVER_PORT", 9090), debug=True)
