import requests as req

import moodle_config as moodle

from utilities import logger, ErrorAPI

log = logger('moodle')


def res(r):
    if r.status_code != 200:
        log.info(r.status_code, exc_info=True)
        raise ErrorAPI(500, r.status_code)

    result = r.json()
    if 'errorcode' in result and result['errorcode']:
        log.info(result['errorcode'], exc_info=True)
        return {}

    return result


def user_info(username):
    url = f'{moodle.URL}/webservice/rest/server.php'
    params = {
        'moodlewsrestformat': 'json',
        'wstoken': moodle.WSTOKEN,
        'wsfunction': moodle.USER_INFO,
        'username': username
    }
    r = req.get(url, params=params)
    user = res(r)
    if user:
        return user[0]
    return {}


def token_info(token):
    url = f'{moodle.URL}/webservice/rest/server.php'
    params = {
        'moodlewsrestformat': 'json',
        'wstoken': token,
        'wsfunction': moodle.TOKEN_INFO
    }
    r = req.get(url, params=params)
    return res(r)


def login(username, password):
    url = f'{moodle.URL}/login/token.php'
    params = {
        'moodlewsrestformat': 'json',
        'service': 'moodle_mobile_app',
        'username': username,
        'password': password
    }
    r = req.get(url, params=params)
    return res(r)


def checkin(roomid, username):
    url = f'{moodle.URL}/webservice/rest/server.php'
    params = {
        'moodlewsrestformat': 'json',
        'wstoken': moodle.WSTOKEN,
        'wsfunction': moodle.CHECKIN,
        'roomid': roomid,
        'username': username
    }
    r = req.post(url, params=params)
    return bool(res(r))


def room_schedule(roomid, date):
    url = f'{moodle.URL}/webservice/rest/server.php'
    params = {
        'moodlewsrestformat': 'json',
        'wstoken': moodle.WSTOKEN,
        'wsfunction': moodle.ROOM_SCHEDULE,
        'roomid': roomid,
        'date': date
    }
    r = req.get(url, params=params)
    return res(r)


def session(sessionid):
    url = f'{moodle.URL}/webservice/rest/server.php'
    params = {
        'moodlewsrestformat': 'json',
        'wstoken': moodle.WSTOKEN,
        'wsfunction': moodle.SESSION,
        'sessionid': sessionid
    }
    r = req.get(url, params=params)
    return res(r)


def reports(attendanceid):
    url = f'{moodle.URL}/webservice/rest/server.php'
    params = {
        'moodlewsrestformat': 'json',
        'wstoken': moodle.WSTOKEN,
        'wsfunction': moodle.GET_LOG,
        'attendanceid': attendanceid
    }
    r = req.get(url, params=params)
    return res(r)


def student_log(username, courseid):
    url = f'{moodle.URL}/webservice/rest/server.php'
    params = {
        'moodlewsrestformat': 'json',
        'wstoken': moodle.WSTOKEN,
        'wsfunction': moodle.GET_STUDENT_LOG,
        'username': username,
        'courseid': courseid
    }
    r = req.get(url, params=params)
    user = res(r)
    if user:
        return user[0]
    return {}


def log_by_course(courseid):
    url = f'{moodle.URL}/webservice/rest/server.php'
    params = {
        'moodlewsrestformat': 'json',
        'wstoken': moodle.WSTOKEN,
        'wsfunction': moodle.GET_LOG_BY_COURSE,
        'courseid': courseid
    }
    r = req.get(url, params=params)
    return res(r)


def room_by_campus(campusid):
    url = f'{moodle.URL}/webservice/rest/server.php'
    params = {
        'moodlewsrestformat': 'json',
        'wstoken': moodle.WSTOKEN,
        'wsfunction': moodle.ROOM_BY_CAMPUS,
        'campus': campusid
    }
    r = req.get(url, params=params)
    return res(r)


def schedules(token, userid):
    url = f'{moodle.URL}/webservice/rest/server.php'
    params = {
        'moodlewsrestformat': 'json',
        'wstoken': token,
        'wsfunction': moodle.GET_COURSE,
        'userid': userid
    }
    r = req.get(url, params=params)
    return res(r)


def create_feedback(roomid,
                    usertaken,
                    userbetaken,
                    description,
                    image):
    url = f'{moodle.URL}/webservice/rest/server.php'
    params = {
        'moodlewsrestformat': 'json',
        'wstoken': moodle.WSTOKEN,
        'wsfunction': moodle.CREATE_FEEDBACK,
        'roomid': roomid,
        'usertaken': usertaken,
        'userbetaken': userbetaken,
        'description': description,
        'image': image
    }
    r = req.post(url, params=params)
    return res(r)


def create_image(username, image_front, image_left, image_right):
    url = f'{moodle.URL}/webservice/rest/server.php'
    data = {
        'moodlewsrestformat': 'json',
        'wstoken': moodle.WSTOKEN,
        'wsfunction': moodle.CREATE_IMAGE,
        'username': username,
        'image_front': image_front,
        'image_left': image_left,
        'image_right': image_right
    }
    r = req.post(url, data=data)
    return res(r)


def get_image(username):
    url = f'{moodle.URL}/webservice/rest/server.php'
    params = {
        'moodlewsrestformat': 'json',
        'wstoken': moodle.WSTOKEN,
        'wsfunction': moodle.GET_IMAGE,
        'username': username
    }
    r = req.post(url, params=params)
    data = res(r)
    if data:
        return data[0]
    return {}
