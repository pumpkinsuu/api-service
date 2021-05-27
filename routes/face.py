from flask import Blueprint, request

from routes.api import verify
import services.face as face
import services.moodle as moodle
from utilities import ErrorAPI, response, logger
log = logger('face')


face_bp = Blueprint('face_bp', __name__)


@face_bp.route('/<collection>', methods=['GET'])
def get_users(collection: str):
    try:
        verify(request.args)

        res = face.users(collection)
        if 'error' in res:
            raise ErrorAPI(
                res['error']['code'],
                res['error']['message']
            )
        return response(200, 'success', res)
    except ErrorAPI as err:
        raise err
    except Exception as ex:
        log.info(str(ex), exc_info=True)
        raise ErrorAPI(500, str(ex))


@face_bp.route('/<collection>', methods=['POST'])
def rename_collection(collection: str):
    try:
        verify(request.args, admin=True)

        if 'name' not in request.json:
            raise ErrorAPI(400, 'missing "name"')
        res = face.rename(
            collection,
            request.json['name']
        )
        if 'error' in res:
            raise ErrorAPI(
                res['error']['code'],
                res['error']['message']
            )
        return response(200, 'success', res)
    except ErrorAPI as err:
        raise err
    except Exception as ex:
        log.info(str(ex), exc_info=True)
        raise ErrorAPI(500, str(ex))


@face_bp.route('/<collection>', methods=['DELETE'])
def drop_collection(collection: str):
    try:
        verify(request.args, admin=True)

        res = face.drop(collection)
        if 'error' in res:
            raise ErrorAPI(
                res['error']['code'],
                res['error']['message']
            )
        return response(200, 'success', res)
    except ErrorAPI as err:
        raise err
    except Exception as ex:
        log.info(str(ex), exc_info=True)
        raise ErrorAPI(500, str(ex))


@face_bp.route('/<collection>/<userID>', methods=['GET'])
def get_user(collection: str, userID: str):
    try:
        verify(request.args)

        res = face.exist(collection, userID)
        if 'error' in res:
            raise ErrorAPI(
                res['error']['code'],
                res['error']['message']
            )
        user = {}
        data = moodle.get_image(userID)
        user['front'] = data['image_front']
        user['left'] = data['image_left']
        user['right'] = data['image_right']

        return response(200, 'success', user)
    except ErrorAPI as err:
        raise err
    except Exception as ex:
        log.info(str(ex), exc_info=True)
        raise ErrorAPI(500, str(ex))


@face_bp.route('/<collection>/<username>', methods=['POST', 'PUT'])
def update_user(collection: str, username: str):
    try:
        verify(request.args, admin=True)

        if 'front' not in request.form:
            raise ErrorAPI(400, 'missing "front"')
        if 'left' not in request.form:
            raise ErrorAPI(400, 'missing "left"')
        if 'right' not in request.form:
            raise ErrorAPI(400, 'missing "right"')

        if not moodle.user_info(username):
            raise ErrorAPI(404, 'user not found')

        res = face.exist(collection, username)
        user = {
            'id': username,
            'front': request.form['front'],
            'left': request.form['left'],
            'right': request.form['right']
        }
        if 'error' in res:
            code = 201
            message = 'created'
            res = face.create(collection, user)
        else:
            code = 200
            message = 'success'
            res = face.update(collection, user)

        if 'error' in res:
            raise ErrorAPI(
                res['error']['code'],
                res['error']['message']
            )
        if code == 200 or code == 201:
            res = moodle.create_image(
                username=user['id'],
                image_front=user['front'],
                image_left=user['left'],
                image_right=user['right']
            )
            if not res:
                code = 500
                message = 'failed to create image'
                face.remove(collection, username)

        return response(code, message)
    except ErrorAPI as err:
        raise err
    except Exception as ex:
        log.info(str(ex), exc_info=True)
        raise ErrorAPI(500, str(ex))


@face_bp.route('/<collection>/<userID>', methods=['DELETE'])
def remove(collection: str, userID: str):
    try:
        verify(request.args, admin=True)

        res = face.remove(collection, userID)
        if 'error' in res:
            raise ErrorAPI(
                res['error']['code'],
                res['error']['message']
            )
        return response(200, 'success')
    except ErrorAPI as err:
        raise err
    except Exception as ex:
        log.info(str(ex), exc_info=True)
        raise ErrorAPI(500, str(ex))


@face_bp.route('/checkin/<roomid>', methods=['POST'])
def check(roomid):
    try:
        verify(request.args)

        if 'collection' not in request.json:
            raise ErrorAPI(400, 'missing "collection"')
        if 'images' not in request.json:
            raise ErrorAPI(400, 'missing "images"')
        if not isinstance(request.json['images'], list):
            raise ErrorAPI(400, '"images" type list')

        userIDs = face.find(
            request.json['collection'],
            request.json['images']
        )
        if not userIDs:
            raise ErrorAPI(400, 'database empty')
        if 'error' in userIDs:
            raise ErrorAPI(
                userIDs['error']['code'],
                userIDs['error']['message']
            )
        users = []
        for userID in userIDs:
            if not userID:
                users.append({
                    'status': 404,
                    'message': 'face not registered'
                })
                continue

            user = moodle.user_info(userID)
            user['avatar'] = moodle.get_image(userID)['image_front']
            user['status'] = 200
            res = moodle.checkin(
                roomid=roomid,
                username=userID
            )
            if 'status' in res:
                user['status'] = res['status']
            user['message'] = res['message']

            users.append(user)

        return response(200, 'success', users)
    except ErrorAPI as err:
        raise err
    except Exception as ex:
        log.info(str(ex), exc_info=True)
        raise ErrorAPI(500, str(ex))


@face_bp.route('/feedback', methods=['POST'])
def face_feedback():
    try:
        verify(request.args)

        if 'image' not in request.json:
            raise ErrorAPI(400, 'missing "image"')
        if 'collection' not in request.json:
            raise ErrorAPI(400, 'missing "collection"')
        if 'roomid' not in request.json:
            raise ErrorAPI(400, 'missing "roomid"')
        if 'usertaken' not in request.json:
            raise ErrorAPI(400, 'missing "usertaken"')
        if 'userbetaken' not in request.json:
            raise ErrorAPI(400, 'missing "userbetaken"')

        description = 'mistaken in face recognition'
        if 'description' in request.json:
            description = request.json['description']

        res = face.exist(
            request.json['collection'],
            request.json['usertaken']
        )
        if 'error' in res:
            raise ErrorAPI(
                res['error']['code'],
                res['error']['message']
            )
        moodle.create_feedback(
            roomid=request.json['roomid'],
            usertaken=request.json['usertaken'],
            userbetaken=request.json['userbetaken'],
            description=description,
            image=request.json['image']
        )
        return response(200, 'success')
    except ErrorAPI as err:
        raise err
    except Exception as ex:
        log.info(str(ex), exc_info=True)
        raise ErrorAPI(500, str(ex))
