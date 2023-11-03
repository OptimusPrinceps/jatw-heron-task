import flask_cors
from flask import Flask, render_template

from API.uploadapi import upload_api

app = Flask(__name__, template_folder='../../webpage/templates', static_folder='../../webpage/static')
flask_cors.CORS(app, expose_headers='Authorization')

app.register_blueprint(upload_api, url_prefix=f'/api/upload')


@app.route('/', methods=['GET'])
def index():
    return render_template('upload.html')
