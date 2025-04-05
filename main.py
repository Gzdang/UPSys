import datetime
import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from questions import create_questions, backup, save_result

from utils import *

app = Flask(__name__)

log_file = './summary/logs.txt'
f2r = load_json("data/f2r.json")


def log(uid, action, time):
    with open(log_file, 'a') as file:
        file.write('['+uid+'] '+action+' at '+str(time)+'\n')

def get_file(file_md5):
    return os.path.split(f2r[file_md5]["path"])


@app.route('/')
def index():
    return render_template('survey.html')


@app.after_request
def add_cache_control(response):
    if response.content_type.startswith('image'):
        response.cache_control.no_cache = False
        response.cache_control.public = True
        response.cache_control.max_age = 86400
    return response


@app.route('/images/<path:img_md5>')
def get_image(img_md5):
    return send_from_directory(*get_file(img_md5))


@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    uid = data['uid']

    time = datetime.datetime.now()
    print(uid, f'finished the query at {time}.')

    save_result(result=data["answer"], uid=uid)
    log(uid, 'done', time)
    return jsonify({'message': 'Succeeded!'})


@app.route('/api/questions')
def get_questions():
    questions, uid = create_questions()
    time = datetime.datetime.now()
    log(uid, 'start', time)
    return jsonify({"uid": uid, "data": questions})


@app.route('/thanks')
def thank_you():
    return render_template('thanks.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

