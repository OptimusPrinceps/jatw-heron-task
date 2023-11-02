import webbrowser

import requests

from API.flask_app import app


def open_frontend():
    local_url = 'http://localhost:4000'
    try:
        running_locally = requests.get(local_url, timeout=0.1)
    except requests.exceptions.RequestException:
        running_locally = False

    base_url = local_url if running_locally else 'https://josh-atwal.com'
    url_to_open = f'{base_url}/portfolio/heron-task.html'
    print("Opening frontend at: ", url_to_open)

    webbrowser.open(url_to_open)


if __name__ == '__main__':
    open_frontend()
    app.run(host='0.0.0.0', debug=True, use_reloader=False)
