from flask import Flask, request
from users.models import User
from app import app


@app.route('/user/singup', methods=['POST'])
def singup():
    data = request.get_json()
    print(data)
    return User().singup(data)
