from flask import Blueprint, request

import services.moodle as moodle

from moodle_config import DEF_ROLE, ADMIN_ROLE
from config import API_KEY
from utilities import ErrorAPI, response, logger
log = logger('api')


def verify(args, admin=False):
    if 'token' not in args:
        raise ErrorAPI(400, 'missing "token"')

    if args['token'] == API_KEY:
        return

    res = moodle.token_info(args['token'])

    user = moodle.user_info(res['username'])
    if not user:
        raise ErrorAPI(404, 'userinfo not found')
    if user['isadmin']:
        return

    role = DEF_ROLE
    if admin:
        role = ADMIN_ROLE

    if not user or user['roleid'] not in role:
        raise ErrorAPI(401, 'no permission')


api_bp = Blueprint('api_bp', __name__)


@api_bp.route('/login', methods=['POST'])
def login():
    try:
        if 'username' not in request.json:
            raise ErrorAPI(400, 'missing "username"')
        if 'password' not in request.json:
            raise ErrorAPI(400, 'missing "password"')

        user = moodle.user_info(request.json['username'])
        if not user:
            raise ErrorAPI(404, 'userinfo not found')

        user['token'] = moodle.login(
            username=request.json['username'],
            password=request.json['password']
        )
        return response(200, 'success', user)
    except ErrorAPI as err:
        raise err
    except Exception as ex:
        log.info(str(ex), exc_info=True)
        raise ErrorAPI(500, str(ex))


@api_bp.route('/get-student-reports', methods=['GET'])
def get_student_log():
    try:
        verify(request.args)

        if 'username' not in request.args:
            raise ErrorAPI(400, 'missing "username"')
        if 'courseid' not in request.args:
            raise ErrorAPI(400, 'missing "courseid"')

        reports = moodle.student_log(
            username=request.args['username'],
            courseid=request.args['courseid']
        )
        return response(200, 'success', reports)
    except ErrorAPI as err:
        raise err
    except Exception as ex:
        log.info(str(ex), exc_info=True)
        raise ErrorAPI(500, str(ex))


@api_bp.route('/get-reports/<courseID>', methods=['GET'])
def get_log_by_course(courseID):
    try:
        verify(request.args)

        reports = moodle.log_by_course(courseID)
        return response(200, 'success', reports)
    except ErrorAPI as err:
        raise err
    except Exception as ex:
        log.info(str(ex), exc_info=True)
        raise ErrorAPI(500, str(ex))


@api_bp.route('/room-schedules', methods=['GET'])
def room_schedule():
    try:
        verify(request.args)

        if 'roomid' not in request.args:
            raise ErrorAPI(400, 'missing "roomid"')
        if 'date' not in request.args:
            raise ErrorAPI(400, 'missing "date"')

        schedule = moodle.room_schedule(
            roomid=request.args['roomid'],
            date=request.args['date']
        )
        return response(200, 'success', schedule)
    except ErrorAPI as err:
        raise err
    except Exception as ex:
        log.info(str(ex), exc_info=True)
        raise ErrorAPI(500, str(ex))


@api_bp.route('/rooms', methods=['GET'])
def get_rooms():
    try:
        verify(request.args)

        if 'campus' not in request.args:
            raise ErrorAPI(400, 'missing "campus"')

        rooms = moodle.room_by_campus(request.args['campus'])
        return response(200, 'success', rooms)
    except ErrorAPI as err:
        raise err
    except Exception as ex:
        log.info(str(ex), exc_info=True)
        raise ErrorAPI(500, str(ex))


@api_bp.route('/teacher-schedules', methods=['GET'])
def get_schedules():
    try:
        verify(request.args)

        user = moodle.token_info(request.args['token'])
        schedules = moodle.schedules(
            token=request.args['token'],
            userid=user['userid']
        )
        return response(200, 'success', schedules)
    except ErrorAPI as err:
        raise err
    except Exception as ex:
        log.info(str(ex), exc_info=True)
        raise ErrorAPI(500, str(ex))


@api_bp.route('/session/<sessionid>', methods=['GET'])
def get_session(sessionid):
    try:
        verify(request.args)

        session = moodle.session(sessionid)
        return response(200, 'success', session)
    except ErrorAPI as err:
        raise err
    except Exception as ex:
        log.info(str(ex), exc_info=True)
        raise ErrorAPI(500, str(ex))


@api_bp.route('/update-attendance-log/<sessionid>', methods=['POST'])
def manual_check(sessionid):
    try:
        verify(request.args)

        if 'students' not in request.json:
            raise ErrorAPI(400, 'missing "students"')
        if not isinstance(request.json['students'], list):
            raise ErrorAPI(400, '"students" type list')

        for student in request.json['students']:
            moodle.update_log(
                sessionid=sessionid,
                username=student['username'],
                statusid=student['statusid']
            )
        return response(200, 'success')
    except ErrorAPI as err:
        raise err
    except Exception as ex:
        log.info(str(ex), exc_info=True)
        raise ErrorAPI(500, str(ex))


@api_bp.route('/students/<username>', methods=['GET'])
def get_student(username):
    try:
        verify(request.args)

        user = moodle.user_info(username)
        if not user:
            raise ErrorAPI(404, 'userinfo not found')
        return response(200, 'success', user)
    except ErrorAPI as err:
        raise err
    except Exception as ex:
        log.info(str(ex), exc_info=True)
        raise ErrorAPI(500, str(ex))


@api_bp.route('/campus', methods=['GET'])
def get_campus():
    try:
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
    except ErrorAPI as err:
        raise err
    except Exception as ex:
        log.info(str(ex), exc_info=True)
        raise ErrorAPI(500, str(ex))
