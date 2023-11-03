import webbrowser

from API.flaskapp import app

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:5000')
    app.run(host='0.0.0.0', debug=True, use_reloader=False)
