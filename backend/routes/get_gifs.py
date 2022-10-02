from flask import request, send_file
import base64
from PIL import Image
import io
import numpy as np
import tempfile
from processing import convert_image as converter
from processing import create_gif
from bson.objectid import ObjectId
from app import app, db
import gridfs

@app.route('/get_gifs/<token>', methods=['GET'])
def get_gifs(token):
    dataBase = db.users_gifs.fs.files
    links = []
    for i in dataBase.find({'name': token}):
        print(i["_id"])
        links.append(f'http://127.0.0.1:5000/get_gif/{i["_id"]}')
    print(links)
    return {'status': 'ok', 'links': links}, 200

@app.route('/get_gif/<token>', methods=['GET'])
def get_gif(token):
    dataBase = db.users_gifs
    fs = gridfs.GridFS(dataBase)
    gif = fs.find_one({'_id': ObjectId(token)})
    with tempfile.NamedTemporaryFile(mode="wb", suffix='.gif') as gifFile:
        gifFile.write(gif.read())
        return send_file(gifFile.name, mimetype='image/gif')