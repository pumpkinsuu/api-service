from flask import Flask
from flask_cors import CORS

from config.admin import *

from routes.admin import create_admin_bp
from utilities import ErrorAPI, logger, response
log = logger()

app = Flask(__name__)
CORS(app)
app.secret_key = SECRET


@app.errorhandler(ErrorAPI)
def error_api(e: ErrorAPI):
    return e.detail()


@app.errorhandler(Exception)
def exception(e):
    log.exception()
    return response(500, e)


admin_bp = create_admin_bp(app)
CORS(admin_bp)
app.register_blueprint(admin_bp, url_prefix='/')


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
