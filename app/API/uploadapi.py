import json

import pandas as pd
from flask import Blueprint, jsonify, request, Response
from werkzeug.datastructures import FileStorage

from Skeleton.constants import get_data_dir
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


def parse_json(json_data: dict or str) -> pd.DataFrame:
    if isinstance(json_data, str):
        json_data: dict = json.loads(json_data)
    if 'transactions' in json_data:
        json_data = json_data['transactions']

    df = pd.DataFrame.from_dict(json_data)
    return df


class PostUploadApiMapper:
    @classmethod
    def map_request(cls) -> pd.DataFrame:
        if request.content_type == 'application/json':
            df = parse_json(request.json)
        elif request.content_type.startswith('multipart/form-data'):
            df = parse_file(request.files['file'])
        else:
            raise ApiUserException("Unsupported Media Type.")

        return df

    @classmethod
    def map_response(cls, df: pd.DataFrame) -> Response:
        df_sample = df.head(5)
        df_dict = df_sample.to_dict(orient='records')
        return jsonify(df_dict)


@upload_api.route('/', methods=['POST'])
def upload():
    df = PostUploadApiMapper.map_request()

    df.to_csv(get_data_dir() + '/upload.csv', index=False)

    return PostUploadApiMapper.map_response(df)
