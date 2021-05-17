from PIL import Image
from base64 import b64decode
from io import BytesIO
import time
import logging
from flask import jsonify


def load_img(file):
    img = Image.open(BytesIO(b64decode(file)))
    return img


def time_now():
    return int(time.time())


def logger(file):
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    file = logging.FileHandler(f'{file}.log', mode='w+')
    file.setFormatter(
        logging.Formatter(
            '[%(asctime)s] — <%(name)s>: %(message)s',
            '%Y-%m-%d %H:%M:%S'
        )
    )
    log.addHandler(file)
    return log


def response(status, message, data=''):
    return jsonify({
        'status': status,
        'message': message,
        'data': data
    }), 200


class ErrorAPI(Exception):
    def __init__(self, status, message):
        super().__init__()
        self.status = status
        self.message = message

    def detail(self):
        return response(self.status, self.message)
