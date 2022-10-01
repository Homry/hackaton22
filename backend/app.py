import numpy as np
from flask import Flask, request, make_response
from flask_cors import CORS
import pymongo
import base64
from PIL import Image
import io
from processing import convert_image as converter

app = Flask(__name__)
CORS(app)
app.config['Access-Control-Allow-Origin'] = '*'
app.secret_key = b'\xf5\xd9v\xe6$\xa1\xb4N.C0\xcc\xe2\xb5i\x8f'
client = pymongo.MongoClient('localhost', 27017)
db = client.auth

from users import routes


@app.route('/')
def home():
    return 'Home'

@app.route('/convert_image', methods=['POST'])
def convert_image():
    image = request.get_json()
    test = image.split(',')
    print(len(test))
    print(test[0])
    image = base64.b64decode(test[1])
    image = np.asarray(Image.open(io.BytesIO(image)).convert('RGB'))
    print(image.shape)
    image = converter(image)
    response = make_response(image.tobytes())
    response.headers.set('Content-Type', 'application/octet-stream')
    # response.headers.set('Content-Disposition', 'attachment', filename = 'np-array.bin')
    return response
    #return {'image': "test"}

