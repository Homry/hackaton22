from flask import Flask, request, session, jsonify
from users.models import User
from app import app

@app.route('/user/singup', methods=['POST'])
def singup():
    return User().singup(request.get_json())

@app.route('/user/login', methods=['POST'])
def login():
    return User().login(request.get_json())


