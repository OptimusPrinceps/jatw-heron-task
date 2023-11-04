import os


def get_data_dir():
    current_path = os.path.dirname(__file__)
    repo_root = current_path.split(os.path.sep + 'app' + os.path.sep)[0]
    return os.path.join(repo_root, 'data')
