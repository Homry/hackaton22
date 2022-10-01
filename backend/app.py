from flask import Flask
from flask_cors import CORS


app = Flask(__name__)



from users import routes


@app.route('/')
def home():
    return 'Home'

