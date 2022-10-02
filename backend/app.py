from flask import Flask
from flask_cors import CORS
import pymongo


app = Flask(__name__)
CORS(app)
app.config['Access-Control-Allow-Origin'] = '*'
app.secret_key = b'\xf5\xd9v\xe6$\xa1\xb4N.C0\xcc\xe2\xb5i\x8f'
client = pymongo.MongoClient('localhost', 27017)
db = client

from users import routes
from routes import converter_requests, get_gifs


@app.route('/')
def home():
    return 'Home'

@app.route('/getUser/<token>', methods=['GET'])
def get_user(token):
    user = db.auth.users.find_one({'_id': token})
    return {'user': user}, 200

