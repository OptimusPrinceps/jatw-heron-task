import json

import pandas as pd
from flask import Blueprint, jsonify, request, Response

from Skeleton.exceptions import ApiUserException
from Skeleton.fileparser import FileParser

task_api = Blueprint('task_api', __name__)


class PostUploadApiMapper:
    @classmethod
    def map_request(cls) -> pd.DataFrame:
        if request.content_type == 'application/json':
            json_data = request.json
            df = pd.read_json(json_data)
        elif request.content_type.startswith('multipart/form-data'):
            file = request.files['file']
            df = FileParser.parse_file(file)
        else:
            raise ApiUserException("Unsupported Media Type.")

        return df

    @classmethod
    def map_response(cls, df: pd.DataFrame) -> Response:
        df_sample = df.head(5)
        json_data = df_sample.to_json(orient='records')
        data = json.loads(json_data)
        return jsonify(data)


@task_api.route('/upload', methods=['POST'])
def upload():
    df = PostUploadApiMapper.map_request()

    df.to_csv('../Data/upload.csv', index=False)

    return PostUploadApiMapper.map_response(df)
