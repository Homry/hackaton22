from flask import Flask, jsonify, session
from passlib.hash import pbkdf2_sha256
from app import db
import uuid

class User:
    def start_session(self, user):
        del user['password']
        return user, 200

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
            return self.start_session(user)

        return jsonify({'error': "Singup failed"}), 400

    def logout(self, data):
        session.pop(data)
        return 200

    def login(self, data):
        user = db.users.find_one({
            "email": data['email']
        })

        if user and pbkdf2_sha256.verify(data['password'], user['password']):
            return self.start_session(user)
        return jsonify({'error': "Not correct email or password"}), 400

