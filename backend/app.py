import numpy as np
from flask import Flask, request, make_response, send_file
from flask_cors import CORS
import pymongo
import base64
from PIL import Image
import io
import tempfile
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


    if image is not None:
        with tempfile.NamedTemporaryFile(mode="wb", suffix='.png') as jpg:
            image = Image.fromarray(image)
            print(jpg.name)
            image.save(jpg.name)
            return send_file(jpg.name, mimetype='image/gif')


        # response.headers.set('Content-Disposition', 'attachment', filename = 'np-array.bin')

    return {'error': 'not find face in the image'}, 408
    #return {'image': "test"}

