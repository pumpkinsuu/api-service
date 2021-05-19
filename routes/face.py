from flask import Blueprint, request

from routes.api import verify
import services.face as face
import services.moodle as moodle
from utilities import ErrorAPI, response


face_bp = Blueprint('face_bp', __name__)


@face_bp.route('/<collection>', methods=['GET'])
def get_users(collection: str):
    verify(request.args)

    res = face.users(collection)
    if not res:
        raise ErrorAPI(500, 'something wrong')
    if 'error' in res:
        raise ErrorAPI(
            res['error']['code'],
            res['error']['message']
        )

    return response(200, 'success', res)


@face_bp.route('/<collection>', methods=['POST'])
def rename_collection(collection: str):
    verify(request.args, admin=True)

    if 'name' not in request.json:
        raise ErrorAPI(400, 'missing "name"')
    res = face.rename(
        collection,
        request.json['name']
    )
    if not res:
        raise ErrorAPI(500, 'something wrong')
    if 'error' in res:
        raise ErrorAPI(
            res['error']['code'],
            res['error']['message']
        )

    return response(200, 'success', res)


@face_bp.route('/<collection>', methods=['DELETE'])
def drop_collection(collection: str):
    verify(request.args, admin=True)

    res = face.drop(collection)
    if not res:
        raise ErrorAPI(500, 'something wrong')
    if 'error' in res:
        raise ErrorAPI(
            res['error']['code'],
            res['error']['message']
        )

    return response(200, 'success', res)


@face_bp.route('/<collection>/<userID>', methods=['GET'])
def get_user(collection: str, userID: str):
    verify(request.args)

    res = face.exist(collection, userID)
    if not res:
        raise ErrorAPI(500, 'something wrong')
    if 'error' in res:
        raise ErrorAPI(
            res['error']['code'],
            res['error']['message']
        )

    data = moodle.get_image(userID)
    if data:
        res['front'] = data['image_front']
        res['left'] = data['image_left']
        res['right'] = data['image_right']

    return response(200, 'success', res)


@face_bp.route('/<collection>/<userID>', methods=['POST', 'PUT'])
def update_user(collection: str, userID: str):
    verify(request.args, admin=True)

    if 'front' not in request.form:
        raise ErrorAPI(400, 'missing "front"')
    if 'left' not in request.form:
        raise ErrorAPI(400, 'missing "left"')
    if 'right' not in request.form:
        raise ErrorAPI(400, 'missing "right"')

    if not moodle.user_info(userID):
        raise ErrorAPI(404, 'user not found')

    res = face.exist(collection, userID)
    if not res:
        raise ErrorAPI(500, 'something wrong')

    user = {
        'id': userID,
        'front': request.form['front'],
        'left': request.form['left'],
        'right': request.form['right']
    }

    if 'error' not in res:
        code = 201
        message = 'created'
        res = face.create(collection, user)
    else:
        code = 200
        message = 'success'
        res = face.update(collection, user)

    if not res:
        raise ErrorAPI(500, 'something wrong')
    if 'error' in res:
        raise ErrorAPI(
            res['error']['code'],
            res['error']['message']
        )
    return response(code, message)


@face_bp.route('/<collection>/<userID>', methods=['DELETE'])
def remove(collection: str, userID: str):
    verify(request.args, admin=True)

    res = face.remove(collection, userID)
    if not res:
        raise ErrorAPI(500, 'something wrong')
    if 'error' in res:
        raise ErrorAPI(
            res['error']['code'],
            res['error']['message']
        )
    return response(200, 'success')


@face_bp.route('/checkin/<roomID>', methods=['POST'])
def check(roomID: str):
    verify(request.args)

    if 'collection' not in request.json:
        raise ErrorAPI(400, 'missing "collection"')
    if 'images' not in request.json:
        raise ErrorAPI(400, 'missing "images"')

    userIDs = face.find(
        request.json['collection'],
        request.json.getlist('images')
    )

    users = []
    for userID in userIDs:
        if not userID:
            users.append({'status': 0})

        user = moodle.user_info(userID)
        data = moodle.get_image(userID)
        if data:
            user['avatar'] = data['image_front']

        if moodle.checkin(roomID, userID, 1):
            user['status'] = 1
        else:
            user['status'] = 2

        users.append(user)

    return response(200, 'success', users)


@face_bp.route('/feedback', methods=['POST'])
def face_feedback():
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

    description = 'Mistaken in face recognition'
    if 'description' in request.json:
        description = request.json['description']

    res = face.exist(
        request.json['collection'],
        request.json['usertaken']
    )
    if not res:
        raise ErrorAPI(500, 'something wrong')
    if 'error' in res:
        raise ErrorAPI(
            res['error']['code'],
            res['error']['message']
        )

    if not moodle.create_feedback(
            roomid=request.json['roomid'],
            usertaken=request.json['usertaken'],
            userbetaken=request.json['userbetaken'],
            description=description,
            image=request.json['image']
    ):
        raise ErrorAPI(500, 'failed')

    return response(200, 'success')
