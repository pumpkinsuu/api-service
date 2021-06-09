from flask import Blueprint, request

from utilities import ErrorAPI, response


def create_admin_bp(key_db):
    admin_bp = Blueprint('admin_bp', __name__)

    @admin_bp.route('/moodle', methods=['GET'])
    def get():
        data = key_db.get()
        return response(200, data)

    @admin_bp.route('/moodle', methods=['POST'])
    def get_data():
        moodle = request.form.get('moodle')
        wstoken = request.form.get('wstoken')
        key = request.form.get('key')
        if not moodle or not wstoken or not key:
            raise ErrorAPI(400, 'bad request')

        if key_db.get_data({'moodle': moodle}):
            raise ErrorAPI(409, 'moodle registered')

        if not key_db.create(moodle, wstoken, key):
            raise ErrorAPI(500, 'failed')
        return response(200, 'success')

    @admin_bp.route('/moodle', methods=['PUT'])
    def get_data():
        moodle = request.form.get('moodle')
        wstoken = request.form.get('wstoken')
        key = request.form.get('key')
        if not moodle or not wstoken or not key:
            raise ErrorAPI(400, 'bad request')

        if not key_db.get_data({'moodle': moodle}):
            raise ErrorAPI(404, 'moodle not registered')

        if not key_db.update(
                moodle,
                {
                    'wstoken': wstoken,
                    'key': key
                }):
            raise ErrorAPI(500, 'failed')
        return response(200, 'success')

    @admin_bp.route('/moodle', methods=['DELETE'])
    def remove():
        moodle = request.form.get('moodle')
        if not moodle:
            raise ErrorAPI(400, 'bad request')

        if not key_db.remove(moodle):
            raise ErrorAPI(500, 'failed')
        return response(200, 'success')

    return admin_bp
