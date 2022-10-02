from flask import request, send_file
import base64
from PIL import Image
import io
import numpy as np
import tempfile
from processing import convert_image as converter
from processing import create_gif
from app import app, db
import gridfs


def decode_image(raw):
    image = np.asarray(Image.open(io.BytesIO(base64.b64decode(raw.split(',')[1]))).convert('RGB'))
    print(image.shape)
    return converter(image, "red", "cat")


@app.route('/convert_image', methods=['POST'])
def convert_image():
    raw = request.get_json()
    image = decode_image(raw)
    if image is not None:
        with tempfile.NamedTemporaryFile(mode="wb", suffix='.png') as jpg:
            image = Image.fromarray(image)
            print(jpg.name)
            image.save(jpg.name)
            return send_file(jpg.name, mimetype='image/gif')

    return {'error': 'not find face in the image'}, 408


@app.route('/convert_image/<token>', methods=['POST'])
def convert_image_and_save_in_bd(token):
    raw = request.get_json()
    image = decode_image(raw)
    fs = gridfs.GridFS(db)
    if image is not None:
        with tempfile.NamedTemporaryFile(mode="wb", suffix='.png') as jpg:
            image = Image.fromarray(image)
            print(jpg.name)
            image.save(jpg.name)
            with open(jpg.name, 'rb') as file:
                content = file.read()
            fs.put(content, name=token)
            return send_file(jpg.name, mimetype='image/gif')

    return {'error': 'not find face in the image'}, 408


@app.route('/save_gif/<token>', methods=['GET'])
def save_gif(token):
    fs = gridfs.GridFS(db)
    gif = []
    for i in fs.find({'name': token}):
        data = i.read()
        tmp = np.array(Image.open(io.BytesIO(data)).convert('RGB'))
        gif.append(tmp)
    gif = np.array(gif)
    print(gif.shape)
    gif = create_gif(gif)
    


    return {'error': 'not find face in the image'}, 200




