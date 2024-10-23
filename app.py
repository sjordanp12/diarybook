import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)

db = client[DB_NAME]


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    # sample_recieve = request.args.get('sample_give')
    # print(sample_recieve)
    articles = list(db.diary.find({},{'_id': False}))
    return jsonify({'articles' : articles})

@app.route('/diary', methods=['POST'])
def save_diary():
    # sample_recieve = request.form.get('sample_give')
    # print(sample_recieve)
    title_recieve = request.form.get('title_give')
    content_recieve = request.form.get('content_give')

    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')


    file = request.files['file_give']
    extension = file.filename.split('.')[-1]
    filename = f'static/post-{mytime}.{extension}'
    file.save(filename)

    profile = request.files['profile_give']
    extension = file.filename.split('.')[-1]
    profilname = f'static/profile-{mytime}.{extension}'
    profile.save(profilname)

    time = today.strftime('%A-%Y-%m-%d')

    doc = {
        'file': filename,
        'profile': profilname,
        'title': title_recieve,
        'content': content_recieve,
        'time':time
    }

    db.diary.insert_one(doc)
    return jsonify({'message' : 'data saved'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

