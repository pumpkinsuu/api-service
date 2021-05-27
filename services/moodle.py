import requests as req

import moodle_config as moodle

from utilities import logger, ErrorAPI

log = logger('moodle')


def res_handle(r):
    if r.status_code != 200:
        log.info(r.status_code, exc_info=True)
        raise ErrorAPI(500, r.status_code)

    if r.headers['content-type'] != 'application/json':
        log.info(r.headers['content-type'], exc_info=True)
        raise ErrorAPI(500, 'incorrect moodle content-type')

    res = r.json()
    if 'errorcode' in res:
        err = {
            'status': 500,
            'message': res['errorcode']
        }
        if res['errorcode'].isnumeric():
            err['status'] = int(res['errorcode'])
        if 'message' in res:
            err['message'] = res['message']
        return err

    return res


def user_info(username):
    url = f'{moodle.URL}/webservice/rest/server.php'
    params = {
        'moodlewsrestformat': 'json',
        'wstoken': moodle.WSTOKEN,
        'wsfunction': moodle.USER_INFO,
        'username': username
    }
    r = req.get(url, params=params)
    res = res_handle(r)

    if 'status' in res:
        raise ErrorAPI(res['status'], res['message'])
    if res and isinstance(res, list):
        return res[0]
    return {}


def token_info(token):
    url = f'{moodle.URL}/webservice/rest/server.php'
    params = {
        'moodlewsrestformat': 'json',
        'wstoken': token,
        'wsfunction': moodle.TOKEN_INFO
    }
    r = req.get(url, params=params)
    res = res_handle(r)

    if 'status' in res:
        if res['message'] == 'invalidtoken':
            raise ErrorAPI(401, 'unauthorized request')
        raise ErrorAPI(res['status'], res['message'])
    return res


def login(username, password):
    url = f'{moodle.URL}/login/token.php'
    params = {
        'moodlewsrestformat': 'json',
        'service': 'moodle_mobile_app',
        'username': username,
        'password': password
    }
    r = req.post(url, params=params)
    res = res_handle(r)

    if 'status' in res:
        if res['message'] == 'invalidlogin':
            raise ErrorAPI(401, 'wrong username or password')
        raise ErrorAPI(res['status'], res['message'])
    return res['token']


def update_log(sessionid, username, statusid):
    url = f'{moodle.URL}/webservice/rest/server.php'
    params = {
        'moodlewsrestformat': 'json',
        'wstoken': moodle.WSTOKEN,
        'wsfunction': moodle.UPDATE_LOG,
        'sessionid': sessionid,
        'username': username,
        'statusid': statusid
    }
    r = req.post(url, params=params)
    res = res_handle(r)

    if 'status' in res:
        raise ErrorAPI(res['status'], res['message'])
    return res


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
    return res_handle(r)


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
    res = res_handle(r)

    if 'status' in res:
        raise ErrorAPI(res['status'], res['message'])
    return res


def session(sessionid):
    url = f'{moodle.URL}/webservice/rest/server.php'
    params = {
        'moodlewsrestformat': 'json',
        'wstoken': moodle.WSTOKEN,
        'wsfunction': moodle.SESSION,
        'sessionid': sessionid
    }
    r = req.get(url, params=params)
    res = res_handle(r)

    if 'status' in res:
        raise ErrorAPI(res['status'], res['message'])
    return res


def reports(attendanceid):
    url = f'{moodle.URL}/webservice/rest/server.php'
    params = {
        'moodlewsrestformat': 'json',
        'wstoken': moodle.WSTOKEN,
        'wsfunction': moodle.GET_LOG,
        'attendanceid': attendanceid
    }
    r = req.get(url, params=params)
    res = res_handle(r)

    if 'status' in res:
        raise ErrorAPI(res['status'], res['message'])
    return res


def student_log(studentid, courseid):
    url = f'{moodle.URL}/webservice/rest/server.php'
    params = {
        'moodlewsrestformat': 'json',
        'wstoken': moodle.WSTOKEN,
        'wsfunction': moodle.GET_STUDENT_LOG,
        'studentid': studentid,
        'courseid': courseid
    }
    r = req.get(url, params=params)
    res = res_handle(r)

    if 'status' in res:
        raise ErrorAPI(res['status'], res['message'])
    return res


def log_by_course(courseid):
    url = f'{moodle.URL}/webservice/rest/server.php'
    params = {
        'moodlewsrestformat': 'json',
        'wstoken': moodle.WSTOKEN,
        'wsfunction': moodle.GET_LOG_BY_COURSE,
        'courseid': courseid
    }
    r = req.get(url, params=params)
    res = res_handle(r)

    if 'status' in res:
        raise ErrorAPI(res['status'], res['message'])
    return res


def room_by_campus(campus):
    url = f'{moodle.URL}/webservice/rest/server.php'
    params = {
        'moodlewsrestformat': 'json',
        'wstoken': moodle.WSTOKEN,
        'wsfunction': moodle.ROOM_BY_CAMPUS,
        'campus': campus
    }
    r = req.get(url, params=params)
    res = res_handle(r)

    if 'status' in res:
        raise ErrorAPI(res['status'], res['message'])
    return res


def schedules(token, userid):
    url = f'{moodle.URL}/webservice/rest/server.php'
    params = {
        'moodlewsrestformat': 'json',
        'wstoken': token,
        'wsfunction': moodle.GET_COURSE,
        'userid': userid
    }
    r = req.get(url, params=params)
    res = res_handle(r)

    if 'status' in res:
        raise ErrorAPI(res['status'], res['message'])
    return res


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
    res = res_handle(r)

    if 'status' in res:
        raise ErrorAPI(res['status'], res['message'])
    return res


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
    res = res_handle(r)

    if 'status' in res:
        raise ErrorAPI(res['status'], res['message'])
    return res


def get_image(username):
    url = f'{moodle.URL}/webservice/rest/server.php'
    params = {
        'moodlewsrestformat': 'json',
        'wstoken': moodle.WSTOKEN,
        'wsfunction': moodle.GET_IMAGE,
        'username': username
    }
    r = req.post(url, params=params)
    res = res_handle(r)

    if not res:
        raise ErrorAPI(404, 'images not found')
    if 'status' in res:
        raise ErrorAPI(res['status'], res['message'])
    if isinstance(res, list):
        return res[0]
    return res
