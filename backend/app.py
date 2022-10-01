from flask import Flask
from flask_cors import CORS
import pymongo

app = Flask(__name__)
CORS(app)
app.config['Access-Control-Allow-Origin'] = '*'

client = pymongo.MongoClient('localhost', 27017)
db = client.auth
from users import routes


@app.route('/')
def home():
    return 'Home'

