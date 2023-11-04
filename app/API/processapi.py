import pandas as pd
from flask import Blueprint, Response, jsonify

from ML.task import heron_data_task

process_api = Blueprint('process_api', __name__)


class PostProcessApiMapper:
    @classmethod
    def map_request(cls) -> pd.DataFrame:
        pass

    @classmethod
    def map_response(cls, df: pd.DataFrame) -> Response:
        df_dict = df.to_dict(orient='records')
        return jsonify(df_dict)


@process_api.route('/', methods=['POST'])
def process():
    input_df = pd.read_csv('../data/upload.csv')
    df = heron_data_task(input_df)
    return PostProcessApiMapper.map_response(df)
