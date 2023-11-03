import pandas as pd
from werkzeug.datastructures import FileStorage


class FileParser:
    @classmethod
    def parse_file(cls, file: FileStorage) -> pd.DataFrame:
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.filename.endswith('.xlsx'):
            df = pd.read_excel(file)
        elif file.filename.endswith('.json'):
            df = pd.read_json(file)

        return df
