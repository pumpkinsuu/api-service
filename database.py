from pymongo import TEXT, ASCENDING
from flask_pymongo import PyMongo

from config.server import MONGO_URI, KEY_DB
from utilities import logger


class KeyData:
    def __init__(self, app):
        uri = MONGO_URI + KEY_DB
        self.db = PyMongo(app, uri=uri).db.db

        if self.db.count_documents({}) == 0:
            self.db.create_index([('name', TEXT), ('moodle', TEXT), ('key', TEXT)], unique=True)

        self.log = logger()

    def get_data(self, moodle: str):
        if moodle[-1] == '/':
            moodle = moodle[:-1]
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
            self.log.exception(ex)
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
            self.log.exception(ex)
            return True

    def remove(self, name: str):
        data = {'name': name}
        self.db.delete_one(data)

        return self.db.find_one(data)
