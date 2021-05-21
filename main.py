from flask import Flask
from flask_cors import CORS

from config import *

from routes.face import face_bp
from routes.api import api_bp
from utilities import ErrorAPI, response

app = Flask(__name__)
CORS(app)


@app.errorhandler(ErrorAPI)
def error_api(e: ErrorAPI):
    return e.detail()


@app.errorhandler(404)
def page_not_found(e):
    return response(404, 'page not found')


@app.route('/', methods=['GET'])
def root():
    return response(200, 'ok')


CORS(face_bp)
CORS(api_bp)
app.register_blueprint(face_bp, url_prefix='/face')
app.register_blueprint(api_bp, url_prefix='/api')


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
