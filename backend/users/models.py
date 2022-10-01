from flask import Flask, jsonify
from passlib.hash import pbkdf2_sha256
from app import db
import uuid

class User:
    def singup(self, data):
        print(f'data = {data}')
        user = {
            "_id": uuid.uuid4().hex,
            "name": data['name'],
            "email": data['email'],
            "password": data['password'],
        }
        user['password'] = pbkdf2_sha256.encrypt(user['password'])
        if db.users.find_one({'email': user['email']}):
            return jsonify({"error": 'Email address already use'}), 400

        if db.users.insert_one(user):
            return user, 200

        return jsonify({'error': "Singup failed"}), 400
