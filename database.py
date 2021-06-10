from pymongo import MongoClient, TEXT, ASCENDING
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
            self.db.create_index([('name', TEXT), ('moodle', TEXT), ('key', TEXT)], unique=True)

        self.log = logger('keyDB')

    def get_data(self, moodle: str):
        return self.db.find_one({'moodle': moodle})

    def get_by_name(self, name: str):
        return self.db.find_one({'name': name})

    def get(self):
        results = self.db.find().sort([("collection", ASCENDING)])
        return list(results)

    def search(self, keyword):
        results = self.db.find(
            {"$text": {"$search": keyword}},
            {"score": {"$meta": "textScore"}}
        ).sort([("score", {"$meta": "textScore"})])
        return list(results)

    def create(self, name: str, moodle: str, wstoken: str, key: str):
        try:
            self.db.insert_one({
                'name': name,
                'moodle': moodle,
                'wstoken': wstoken,
                'key': key
            })
            return True
        except Exception as ex:
            self.log.info(ex, exc_info=True)
            return False

    def update(self, name: str, moodle: str, wstoken: str, key: str):
        try:
            self.db.update_one(
                {
                    'name': name
                },
                {
                    "$set": {
                        'moodle': moodle,
                        'wstoken': wstoken,
                        'key': key
                    }
                }
            )
            return True
        except Exception as ex:
            self.log.info(ex, exc_info=True)
            return True

    def remove(self, name: str):
        try:
            self.db.delete_one({'name': name})
            return True
        except Exception as ex:
            self.log.info(ex, exc_info=True)
            return False
