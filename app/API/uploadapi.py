import json

import pandas as pd
from flask import Blueprint, jsonify, request, Response
from werkzeug.datastructures import FileStorage

from Skeleton.exceptions import ApiUserException

upload_api = Blueprint('upload_api', __name__)


def parse_file(file: FileStorage) -> pd.DataFrame:
    if file.filename.endswith('.csv'):
        df = pd.read_csv(file)
    elif file.filename.endswith('.xlsx'):
        df = pd.read_excel(file)
    elif file.filename.endswith('.json'):
        df = pd.read_json(file)
    else:
        raise ApiUserException('Unsupported file type.')

    return df


class PostUploadApiMapper:
    @classmethod
    def map_request(cls) -> pd.DataFrame:
        if request.content_type == 'application/json':
            json_data = request.json
            df = pd.read_json(json_data)
        elif request.content_type.startswith('multipart/form-data'):
            file = request.files['file']
            df = parse_file(file)
        else:
            raise ApiUserException("Unsupported Media Type.")

        return df

    @classmethod
    def map_response(cls, df: pd.DataFrame) -> Response:
        df_sample = df.head(5)
        json_data = df_sample.to_json(orient='records')
        data = json.loads(json_data)
        return jsonify(data)


@upload_api.route('/', methods=['POST'])
def upload():
    df = PostUploadApiMapper.map_request()

    df.to_csv('../Data/upload.csv', index=False)

    return PostUploadApiMapper.map_response(df)
