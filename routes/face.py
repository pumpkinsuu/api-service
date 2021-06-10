from flask import Blueprint, request, g

import services.face as face_sv
import services.moodle as moodle_sv
from utilities import ErrorAPI, response


face_bp = Blueprint('face_bp', __name__)


@face_bp.route('/count', methods=['GET'])
def count():
    key = g.key
    res = face_sv.count(key)
    return response(200, 'success', res)


@face_bp.route('/users', methods=['GET'])
def get_user():
    moodle = request.headers['moodle']
    wstoken = g.wstoken
    key = g.key
    username = g.username
    res = face_sv.exist(key, username)
    if 'error' in res:
        raise ErrorAPI(
            res['error']['code'],
            res['error']['message']
        )
    user = {}
    data = moodle.get_image(
        moodle=moodle,
        wstoken=wstoken,
        username=username
    )
    user['front'] = data['image_front']
    user['left'] = data['image_left']
    user['right'] = data['image_right']

    return response(200, 'success', user)


@face_bp.route('/users', methods=['POST', 'PUT'])
def update_user():
    moodle = request.headers['moodle']
    wstoken = g.wstoken
    key = g.key
    username = g.username

    if 'front' not in request.form:
        raise ErrorAPI(400, 'missing "front"')
    if 'left' not in request.form:
        raise ErrorAPI(400, 'missing "left"')
    if 'right' not in request.form:
        raise ErrorAPI(400, 'missing "right"')
    if 'replace' not in request.form:
        replace = 0
    else:
        replace = 1

    if not moodle_sv.user_info(
            moodle=moodle,
            wstoken=wstoken,
            username=username
    ):
        raise ErrorAPI(404, 'user not found')

    res = face_sv.exist(key, username)
    user = {
        'id': username,
        'front': request.form['front'],
        'left': request.form['left'],
        'right': request.form['right']
    }
    if 'error' in res:
        code = 201
        message = 'created'
        res = face_sv.create(key, user)
    else:
        code = 200
        message = 'success'
        res = face_sv.update(key, user)

    if 'error' in res:
        raise ErrorAPI(
            res['error']['code'],
            res['error']['message']
        )
    if code == 200 or code == 201:
        res = moodle_sv.create_image(
            moodle=moodle,
            wstoken=wstoken,
            username=user['id'],
            image_front=user['front'],
            image_left=user['left'],
            image_right=user['right'],
            replace=replace
        )
        if not res:
            code = 500
            message = 'failed to create image'
            face_sv.remove(key, username)

    return response(code, message)


@face_bp.route('/checkin/<roomid>', methods=['POST'])
def check(roomid):
    moodle = request.headers['moodle']
    wstoken = g.wstoken
    key = g.key

    if 'images' not in request.json:
        raise ErrorAPI(400, 'missing "images"')
    if not isinstance(request.json['images'], list):
        raise ErrorAPI(400, '"images" type list')

    usernames = face_sv.find(
        key,
        request.json['images']
    )
    if not usernames:
        raise ErrorAPI(400, 'no user registered')
    if 'error' in usernames:
        raise ErrorAPI(
            usernames['error']['code'],
            usernames['error']['message']
        )
    users = []
    for username in usernames:
        if not username:
            users.append({
                'status': 404,
                'message': 'face not registered'
            })
            continue

        user = moodle_sv.user_info(
            moodle=moodle,
            wstoken=wstoken,
            username=username
        )
        user['status'] = 200
        res = moodle_sv.checkin(
            moodle=moodle,
            wstoken=wstoken,
            roomid=roomid,
            username=username
        )
        if 'status' in res:
            user['status'] = res['status']
        user['message'] = res['message']

        users.append(user)

    return response(200, 'success', users)


@face_bp.route('/feedback', methods=['POST'])
def face_feedback():
    moodle = request.headers['moodle']
    wstoken = g.wstoken
    key = g.key

    if 'image' not in request.json:
        raise ErrorAPI(400, 'missing "image"')
    if 'roomid' not in request.json:
        raise ErrorAPI(400, 'missing "roomid"')
    if 'usertaken' not in request.json:
        raise ErrorAPI(400, 'missing "usertaken"')
    if 'userbetaken' not in request.json:
        raise ErrorAPI(400, 'missing "userbetaken"')

    description = 'mistaken in face recognition'
    if 'description' in request.json:
        description = request.json['description']

    res = face_sv.exist(
        key,
        request.json['usertaken']
    )
    if 'error' in res:
        raise ErrorAPI(
            res['error']['code'],
            res['error']['message']
        )
    moodle_sv.create_feedback(
        moodle=moodle,
        wstoken=wstoken,
        roomid=request.json['roomid'],
        usertaken=request.json['usertaken'],
        userbetaken=request.json['userbetaken'],
        description=description,
        image=request.json['image']
    )
    return response(200, 'success')
