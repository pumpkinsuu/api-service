from flask import Blueprint, request, g

import services.moodle as moodle_sv

from utilities import ErrorAPI, response


api_bp = Blueprint('api_bp', __name__)


@api_bp.route('/login', methods=['POST'])
def login():
    moodle = request.headers['moodle']
    wstoken = g['wstoken']

    if 'username' not in request.json:
        raise ErrorAPI(400, 'missing "username"')
    if 'password' not in request.json:
        raise ErrorAPI(400, 'missing "password"')
    username = request.json['username']
    password = request.json['password']

    user = moodle_sv.user_info(
        moodle=moodle,
        wstoken=wstoken,
        username=username
    )
    if not user:
        raise ErrorAPI(404, 'userinfo not found')

    user['token'] = moodle_sv.login(
        moodle=moodle,
        username=username,
        password=password
    )
    return response(200, 'success', user)


@api_bp.route('/get-student-reports', methods=['GET'])
def get_student_log():
    moodle = request.headers['moodle']
    wstoken = g['wstoken']

    if 'username' not in request.args:
        raise ErrorAPI(400, 'missing "username"')
    if 'courseid' not in request.args:
        raise ErrorAPI(400, 'missing "courseid"')
    username = request.args['username']
    courseid = request.args['courseid']

    reports = moodle_sv.student_log(
        moodle=moodle,
        wstoken=wstoken,
        username=username,
        courseid=courseid
    )
    if not reports:
        reports = None
    return response(200, 'success', reports)


@api_bp.route('/get-reports/<courseid>', methods=['GET'])
def get_log_by_course(courseid):
    moodle = request.headers['moodle']
    wstoken = g['wstoken']

    reports = moodle_sv.log_by_course(
        moodle=moodle,
        wstoken=wstoken,
        courseid=courseid
    )
    if not reports:
        reports = None
    return response(200, 'success', reports)


@api_bp.route('/room-schedules', methods=['GET'])
def room_schedule():
    moodle = request.headers['moodle']
    wstoken = g['wstoken']

    if 'roomid' not in request.args:
        raise ErrorAPI(400, 'missing "roomid"')
    if 'date' not in request.args:
        raise ErrorAPI(400, 'missing "date"')
    roomid = request.args['roomid']
    date = request.args['date']

    schedule = moodle_sv.room_schedule(
        moodle=moodle,
        wstoken=wstoken,
        roomid=roomid,
        date=date
    )
    if not schedule:
        schedule = None
    return response(200, 'success', schedule)


@api_bp.route('/rooms', methods=['GET'])
def get_rooms():
    moodle = request.headers['moodle']
    wstoken = g['wstoken']

    if 'campus' not in request.args:
        raise ErrorAPI(400, 'missing "campus"')
    campus = request.args['campus']

    rooms = moodle_sv.room_by_campus(
        moodle=moodle,
        wstoken=wstoken,
        campus=campus
    )
    if not rooms:
        rooms = None
    return response(200, 'success', rooms)


@api_bp.route('/teacher-schedules', methods=['GET'])
def get_schedules():
    moodle = request.headers['moodle']
    userid = g['userid']
    token = request.headers['token']

    schedules = moodle_sv.schedules(
        moodle=moodle,
        token=token,
        userid=userid
    )
    if not schedules:
        schedules = None
    return response(200, 'success', schedules)


@api_bp.route('/session/<sessionid>', methods=['GET'])
def get_session(sessionid):
    moodle = request.headers['moodle']
    wstoken = g['wstoken']

    session = moodle_sv.session(
        moodle=moodle,
        wstoken=wstoken,
        sessionid=sessionid
    )
    if not session:
        session = None
    return response(200, 'success', session)


@api_bp.route('/sessions/<courseid>', methods=['GET'])
def get_sessions(courseid):
    moodle = request.headers['moodle']
    wstoken = g['wstoken']

    sessions = moodle_sv.sessions(
        moodle=moodle,
        wstoken=wstoken,
        courseid=courseid
    )
    if not sessions:
        sessions = None
    return response(200, 'success', sessions)


@api_bp.route('/update-attendance-log/<sessionid>', methods=['POST'])
def manual_check(sessionid):
    moodle = request.headers['moodle']
    wstoken = g['wstoken']

    if 'students' not in request.json:
        raise ErrorAPI(400, 'missing "students"')
    if not isinstance(request.json['students'], list):
        raise ErrorAPI(400, '"students" type list')
    students = request.json['students']

    for student in students:
        moodle_sv.update_log(
            moodle=moodle,
            wstoken=wstoken,
            sessionid=sessionid,
            username=student['username'],
            statusid=student['statusid']
        )
    return response(200, 'success')


@api_bp.route('/students/<username>', methods=['GET'])
def get_student(username):
    moodle = request.headers['moodle']
    wstoken = g['wstoken']

    user = moodle_sv.user_info(
        moodle=moodle,
        wstoken=wstoken,
        username=username
    )
    if not user:
        raise ErrorAPI(404, 'userinfo not found')
    return response(200, 'success', user)


@api_bp.route('/campus', methods=['GET'])
def get_campus():
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
