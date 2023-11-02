from flask import Flask
from API.routes import task_api

app = Flask(__name__)

app.register_blueprint(task_api, url_prefix='/task')
