from flask import Flask, request, g
from flask_cors import CORS
from time import time

from config.server import *
from config.moodle import ROLE
from database import KeyData
from routes.face import face_bp
from routes.api import api_bp
from services.moodle import token_info, user_info
from utilities import ErrorAPI, response, logger
log = logger('error')

app = Flask(__name__)
CORS(app)


key_db = KeyData(app)


@app.errorhandler(ErrorAPI)
def error_api(e: ErrorAPI):
    return e.detail()


@app.errorhandler(Exception)
def exception(e):
    log.info(str(e), exc_info=True)
    return response(500, str(e))


@app.before_request
def check_request():
    g.start = time()

    if 'moodle' not in request.headers:
        raise ErrorAPI(400, 'no moodle provided')
    moodle = request.headers['moodle']
    # Check moodle
    data = key_db.get_data(moodle)
    if not data:
        raise ErrorAPI(400, 'invalid moodle')
    g.key = data['key']
    g.wstoken = data['wstoken']

    if '/api/login' in request.path:
        return

    if 'Authorization' not in request.headers:
        raise ErrorAPI(400, 'no token provided')
    token = request.headers['Authorization']
    # Check token
    res = token_info(
        moodle=moodle,
        token=token
    )
    g.username = res['username']
    g.userid = res['userid']

    user = user_info(
        moodle=moodle,
        wstoken=g.wstoken,
        username=res['username']
    )
    if not user:
        raise ErrorAPI(404, 'userinfo not found')
    # Check role
    if USER_ROUTES in request.path:
        return
    if user['isadmin']:
        return
    if user['roleid'] not in ROLE:
        raise ErrorAPI(401, 'no permission')


@app.route('/', methods=['GET'])
def root():
    return response(200, 'ok')


CORS(face_bp)
CORS(api_bp)
app.register_blueprint(face_bp, url_prefix='/face')
app.register_blueprint(api_bp, url_prefix='/api')


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
