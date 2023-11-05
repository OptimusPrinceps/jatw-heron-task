import os


def get_data_dir():
    """
    :return: Path to the directory containing data files without the trailing slash.
    """
    current_path = os.path.dirname(__file__)
    repo_root = current_path.split(os.path.sep + 'app' + os.path.sep)[0]
    return os.path.join(repo_root, 'data')
