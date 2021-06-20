from PIL import Image
from base64 import b64decode
from io import BytesIO
import logging
from flask import jsonify


def load_img(file):
    img = Image.open(BytesIO(b64decode(file)))
    return img


def logger():
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    file = logging.FileHandler('error.log', mode='w+')
    file.setFormatter(
        logging.Formatter(
            '[%(asctime)s] — <%(name)s>: %(message)s',
            '%Y-%m-%d %H:%M:%S'
        )
    )
    log.addHandler(file)
    return log


def response(status, message, data=None, service='api', t=None):
    return jsonify({
        'status': status,
        'message': message,
        'data': data,
        'service': service,
        'time': t
    }), 200


class ErrorAPI(Exception):
    def __init__(self, status, message, service='api'):
        super().__init__()
        self.status = status
        self.message = message
        self.service = service

    def detail(self):
        return response(self.status, self.message, service=self.service)
