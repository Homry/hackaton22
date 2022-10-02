from flask import request, send_file, send_from_directory
import tempfile

from bson.objectid import ObjectId
from app import app, db
import gridfs

@app.route('/get_gifs/<token>', methods=['GET'])
def get_gifs(token):
    dataBase = db.users_gifs.fs.files
    links = []
    downloads = []
    for i in dataBase.find({'name': token}):
        links.append(f'http://127.0.0.1:5000/get_gif/{i["_id"]}')
        downloads.append(f'http://127.0.0.1:5000/download/{i["_id"]}')
    return {'status': 'ok', 'links': links, 'download': downloads}, 200

@app.route('/get_gif/<token>', methods=['GET'])
def get_gif(token):
    print(token)
    dataBase = db.users_gifs
    fs = gridfs.GridFS(dataBase)
    gif = fs.find_one({'_id': ObjectId(token)})
    with tempfile.NamedTemporaryFile(mode="wb", suffix='.gif') as gifFile:
        gifFile.write(gif.read())
        return send_file(gifFile.name, mimetype='image/gif')

@app.route('/download/<token>', methods=['GET', 'POST'])
def download(token):
    dataBase = db.users_gifs
    fs = gridfs.GridFS(dataBase)
    gif = fs.find_one({'_id': ObjectId(token)})
    with tempfile.NamedTemporaryFile(mode="wb", suffix='.gif') as gifFile:
        gifFile.write(gif.read())
        print(gifFile.name)
        names = gifFile.name.split('/')
        filename = names[-1]
        names.pop(-1)
        directory = '/'.join(names)

        return send_file(gifFile.name,  mimetype='image/gif')