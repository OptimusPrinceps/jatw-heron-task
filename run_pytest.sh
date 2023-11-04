#!/bin/bash
set -e

pip install flake8

# stop the build if there are Python syntax errors or undefined names
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
# exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics


# check if file doesnt exist
if [ ! -f "./data/mydata.csv" ]; then
  python app/Utils/create_mock_data.py
fi

cd app
python3 -m pytest
