from flask import Blueprint, request

import services.moodle as moodle
from utilities import ErrorAPI, response

from moodle_config import DEF_ROLE, ADMIN_ROLE
from config import API_KEY


def verify(args, admin=False):
    if 'token' not in args:
        raise ErrorAPI(400, 'missing "token"')

    if args['token'] == API_KEY:
        return

    result = moodle.token_info(args['token'])
    if not result:
        raise ErrorAPI(401, 'unauthorized request')

    if result['userissiteadmin']:
        return

    role = DEF_ROLE
    if admin:
        role = ADMIN_ROLE

    user = moodle.user_info(result['username'])
    if not user or user['roleid'] not in role:
        raise ErrorAPI(401, 'no permission')


api_bp = Blueprint('api_bp', __name__)


@api_bp.route('/login', methods=['POST'])
def login():
    if 'username' not in request.json:
        raise ErrorAPI(400, 'missing "username"')
    if 'password' not in request.json:
        raise ErrorAPI(400, 'missing "password"')

    result = moodle.login(request.json['username'], request.json['password'])
    if not result:
        raise ErrorAPI(401, 'wrong username or password')

    user = moodle.user_info(request.json['username'])
    user['token'] = result['token']

    return response(200, 'success', user)


@api_bp.route('/get-student-reports ', methods=['GET'])
def get_student_log():
    verify(request.args)

    if 'studentid' not in request.args:
        raise ErrorAPI(400, 'missing "studentid"')
    if 'courseid' not in request.args:
        raise ErrorAPI(400, 'missing "courseid"')

    reports = moodle.student_log(request.args['studentid'], request.args['courseid'])
    if not reports:
        raise ErrorAPI(404, 'student\'s report not found')

    return response(200, 'success', reports)


@api_bp.route('/get-reports/<courseID>', methods=['GET'])
def get_log_by_course(courseID):
    verify(request.args)

    reports = moodle.log_by_course(courseID)
    if not reports:
        raise ErrorAPI(404, 'course not found')

    return response(200, 'success', reports)


@api_bp.route('/room-schedules', methods=['GET'])
def room_schedule():
    verify(request.args)

    if 'roomid' not in request.args:
        raise ErrorAPI(400, 'missing "roomid"')
    if 'date' not in request.args:
        raise ErrorAPI(400, 'missing "date"')

    schedule = moodle.room_schedule(
        request.args['roomid'],
        request.args['date']
    )
    if not schedule:
        raise ErrorAPI(404, 'schedule not found')

    return response(200, 'success', schedule)


@api_bp.route('/rooms', methods=['GET'])
def get_rooms():
    verify(request.args)

    if 'campus' not in request.args:
        raise ErrorAPI(400, 'missing "campus"')

    reports = moodle.room_by_campus(request.args['campus'])
    if not reports:
        raise ErrorAPI(404, 'campus not found')

    return response(200, 'success', reports)


@api_bp.route('/teacher-schedules', methods=['GET'])
def get_schedules():
    verify(request.args)

    user = moodle.token_info(request.args['token'])

    schedules = moodle.schedules(
        request.args['token'],
        user['userid']
    )
    if not schedules:
        raise ErrorAPI(404, 'schedules not found')

    return response(200, 'success', schedules)


@api_bp.route('/session/<sessionID>', methods=['GET'])
def get_session(sessionID):
    verify(request.args)

    session = moodle.session(sessionID)
    if not session:
        raise ErrorAPI(404, 'session not found')

    return response(200, 'success', session)


@api_bp.route('/update-attendance-log/<roomID>', methods=['POST'])
def manual_check(roomID):
    verify(request.args)

    if 'students' not in request.json:
        raise ErrorAPI(400, 'missing "students"')

    for student in request.json['students']:
        if not moodle.checkin(roomID, student['id'], student['status']):
            raise ErrorAPI(400, 'failed to checkin')

    return response(200, 'success')


@api_bp.route('/students/<username>', methods=['GET'])
def get_student(username):
    verify(request.args)

    student = moodle.user_info(username)

    if not student:
        raise ErrorAPI(404, 'username not found')

    data = moodle.get_image(username)
    if data:
        student['front'] = data['image_front']
        student['left'] = data['image_left']
        student['right'] = data['image_right']

    return response(200, 'success', student)


@api_bp.route('/campus', methods=['GET'])
def get_campus():
    verify(request.args)

    campus = [
            {
                'id': 'NVC',
                'name': 'Nguyễn Văn Cừ'
            },
            {
                'id': 'LT',
                'name': 'Linh Trung'
            }
    ]
    return response(200, 'success', campus)
