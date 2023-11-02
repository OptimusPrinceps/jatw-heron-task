import pandas as pd
from flask import Blueprint, request

task_api = Blueprint('task_api', __name__, template_folder='/task')


@task_api.route('/upload', methods=['POST'])
def upload_csv():
    file = request.files['csvfile']
    df = pd.read_csv(file)
    df_json = df.to_json()
    return df_json
