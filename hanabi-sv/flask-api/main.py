import time
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return "Holo"

@app.route('/time')
def time_api():
    return {'time': time.time()}


if __name__ == '__main__':
    app.run(debug=True)
