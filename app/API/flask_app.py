import flask_cors
from flask import Flask

from API.constants import ApiRoutes
from API.routes import task_api

app = Flask(__name__)
flask_cors.CORS(app, expose_headers='Authorization')

app.register_blueprint(task_api, url_prefix=f'/api/{ApiRoutes.TASK_API}')
