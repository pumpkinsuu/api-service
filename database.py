from pymongo import MongoClient, TEXT
from flask_pymongo import PyMongo

from config.server import MONGO_URI, KEY_DB
from utilities import logger


class KeyData:
    def __init__(self, app=None):
        uri = MONGO_URI + KEY_DB
        if app:
            self.db = PyMongo(app, uri=uri).db.db
        else:
            self.db = MongoClient(uri).db

        if self.db.count_documents({}) == 0:
            self.db.create_index([('moodle', TEXT), ('key', TEXT)], unique=True)

        self.log = logger('keyDB')

    def get_data(self, moodle: str):
        return self.db.find_one({'moodle': moodle})

    def get(self):
        results = self.db.find()
        data = []

        for res in results:
            data.append(res)

        return data

    def create(self, moodle: str, wstoken: str, key: str):
        try:
            self.db.insert_one({
                'moodle': moodle,
                'wstoken': wstoken,
                'key': key
            })
            return True
        except Exception as ex:
            self.log.info(ex, exc_info=True)
            return False

    def update(self, moodle: str, data: dict):
        try:
            self.db.update_one(
                {
                    'moodle': moodle
                },
                {
                    "$set": data
                }
            )
            return True
        except Exception as ex:
            self.log.info(ex, exc_info=True)
            return True

    def remove(self, moodle: str):
        try:
            self.db.delete_one({'moodle': moodle})
            return True
        except Exception as ex:
            self.log.info(ex, exc_info=True)
            return False
