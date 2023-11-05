import pandas as pd
from flask import Blueprint, Response, jsonify

from ML.task import identify_recurring_transactions

process_api = Blueprint('process_api', __name__)


class PostProcessApiMapper:
    @classmethod
    def map_request(cls) -> pd.DataFrame:
        pass

    @classmethod
    def map_response(cls, transactions) -> Response:
        return jsonify(transactions)


@process_api.route('/', methods=['POST'])
def process():
    input_df = pd.read_csv('../data/upload.csv')
    transactions = identify_recurring_transactions(input_df)
    return PostProcessApiMapper.map_response(transactions)
