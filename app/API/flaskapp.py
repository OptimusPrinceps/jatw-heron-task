import flask_cors
from flask import Flask, render_template

from API.constants import ApiRoutes
from API.taskapi import task_api

app = Flask(__name__, template_folder='../../frontend/templates', static_folder='../../frontend/static')
flask_cors.CORS(app, expose_headers='Authorization')

app.register_blueprint(task_api, url_prefix=f'/api/{ApiRoutes.TASK_API}')


@app.route('/', methods=['GET'])
def index():
    return render_template('upload.html')
