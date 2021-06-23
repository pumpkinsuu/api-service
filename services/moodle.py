import requests as req

from config.moodle import *

from utilities import logger, ErrorAPI

log = logger()


def res_handle(r):
    if r.status_code != 200:
        log.info(r.status_code, exc_info=True)
        raise ErrorAPI(500, r.status_code, 'moodle')

    if 'application/json' not in r.headers['content-type']:
        log.info(r.headers['content-type'], exc_info=True)
        raise ErrorAPI(500, 'incorrect content-type', 'moodle')

    res = r.json()
    if 'errorcode' in res and res['errorcode']:
        if res['errorcode'] == 'invalidtoken':
            raise ErrorAPI(401, 'invalid/expired token', 'moodle')
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


def user_info(moodle, wstoken, username):
    url = f'{moodle}/webservice/rest/server.php'
    params = {
        'moodlewsrestformat': 'json',
        'wstoken': wstoken,
        'wsfunction': USER_INFO,
        'username': username
    }
    r = req.get(url, params=params)
    res = res_handle(r)

    if 'status' in res:
        raise ErrorAPI(res['status'], res['message'], 'moodle')
    if res and isinstance(res, list):
        return res[0]
    return {}


def token_info(moodle, token):
    url = f'{moodle}/webservice/rest/server.php'
    params = {
        'moodlewsrestformat': 'json',
        'wstoken': token,
        'wsfunction': TOKEN_INFO
    }
    r = req.get(url, params=params)
    res = res_handle(r)

    if 'status' in res:
        raise ErrorAPI(res['status'], res['message'], 'moodle')
    return res


def login(moodle, username, password):
    url = f'{moodle}/login/token.php'
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
            raise ErrorAPI(401, 'wrong username or password', 'moodle')
        raise ErrorAPI(res['status'], res['message'], 'moodle')
    return res['token']


def update_log(moodle, wstoken, sessionid, username, statusid):
    url = f'{moodle}/webservice/rest/server.php'
    params = {
        'moodlewsrestformat': 'json',
        'wstoken': wstoken,
        'wsfunction': UPDATE_LOG,
        'sessionid': sessionid,
        'username': username,
        'statusid': statusid
    }
    r = req.post(url, params=params)
    res = res_handle(r)

    if 'status' in res:
        raise ErrorAPI(res['status'], res['message'], 'moodle')
    return res


def checkin(moodle, wstoken, roomid, username):
    url = f'{moodle}/webservice/rest/server.php'
    params = {
        'moodlewsrestformat': 'json',
        'wstoken': wstoken,
        'wsfunction': CHECKIN,
        'roomid': roomid,
        'username': username
    }
    r = req.post(url, params=params)
    return res_handle(r)


def room_schedule(moodle, wstoken, roomid, date):
    url = f'{moodle}/webservice/rest/server.php'
    params = {
        'moodlewsrestformat': 'json',
        'wstoken': wstoken,
        'wsfunction': ROOM_SCHEDULE,
        'roomid': roomid,
        'date': date
    }
    r = req.get(url, params=params)
    res = res_handle(r)

    if 'status' in res:
        raise ErrorAPI(res['status'], res['message'], 'moodle')
    return res


def session(moodle, wstoken, sessionid):
    url = f'{moodle}/webservice/rest/server.php'
    params = {
        'moodlewsrestformat': 'json',
        'wstoken': wstoken,
        'wsfunction': SESSION,
        'sessionid': sessionid
    }
    r = req.get(url, params=params)
    res = res_handle(r)

    if 'status' in res:
        raise ErrorAPI(res['status'], res['message'], 'moodle')
    return res


def sessions(moodle, wstoken, courseid):
    url = f'{moodle}/webservice/rest/server.php'
    params = {
        'moodlewsrestformat': 'json',
        'wstoken': wstoken,
        'wsfunction': SESSIONS,
        'courseid': courseid
    }
    r = req.get(url, params=params)
    res = res_handle(r)

    if 'status' in res:
        raise ErrorAPI(res['status'], res['message'], 'moodle')
    return res


def reports(moodle, wstoken, attendanceid):
    url = f'{moodle}/webservice/rest/server.php'
    params = {
        'moodlewsrestformat': 'json',
        'wstoken': wstoken,
        'wsfunction': GET_LOG,
        'attendanceid': attendanceid
    }
    r = req.get(url, params=params)
    res = res_handle(r)

    if 'status' in res:
        raise ErrorAPI(res['status'], res['message'], 'moodle')
    return res


def student_log(moodle, wstoken, username, courseid):
    url = f'{moodle}/webservice/rest/server.php'
    params = {
        'moodlewsrestformat': 'json',
        'wstoken': wstoken,
        'wsfunction': GET_STUDENT_LOG,
        'username': username,
        'courseid': courseid
    }
    r = req.get(url, params=params)
    res = res_handle(r)

    if 'status' in res:
        raise ErrorAPI(res['status'], res['message'], 'moodle')
    return res


def log_by_course(moodle, wstoken, courseid):
    url = f'{moodle}/webservice/rest/server.php'
    params = {
        'moodlewsrestformat': 'json',
        'wstoken': wstoken,
        'wsfunction': GET_LOG_BY_COURSE,
        'courseid': courseid
    }
    r = req.get(url, params=params)
    res = res_handle(r)

    if 'status' in res:
        raise ErrorAPI(res['status'], res['message'], 'moodle')
    return res


def room_by_campus(moodle, wstoken, campus):
    url = f'{moodle}/webservice/rest/server.php'
    params = {
        'moodlewsrestformat': 'json',
        'wstoken': wstoken,
        'wsfunction': ROOM_BY_CAMPUS,
        'campus': campus
    }
    r = req.get(url, params=params)
    res = res_handle(r)

    if 'status' in res:
        raise ErrorAPI(res['status'], res['message'], 'moodle')
    return res


def schedules(moodle, token, userid):
    url = f'{moodle}/webservice/rest/server.php'
    params = {
        'moodlewsrestformat': 'json',
        'wstoken': token,
        'wsfunction': GET_COURSE,
        'userid': userid
    }
    r = req.get(url, params=params)
    res = res_handle(r)

    if 'status' in res:
        raise ErrorAPI(res['status'], res['message'], 'moodle')
    return res


def create_feedback(moodle,
                    wstoken,
                    roomid,
                    usertaken,
                    userbetaken,
                    description,
                    image):
    url = f'{moodle}/webservice/rest/server.php'
    params = {
        'moodlewsrestformat': 'json',
        'wstoken': wstoken,
        'wsfunction': CREATE_FEEDBACK,
        'roomid': roomid,
        'usertaken': usertaken,
        'userbetaken': userbetaken,
        'description': description,
        'image': image
    }
    r = req.post(url, params=params)
    res = res_handle(r)

    if 'status' in res:
        raise ErrorAPI(res['status'], res['message'], 'moodle')
    return res


def create_image(moodle,
                 wstoken,
                 username,
                 image_front,
                 image_left,
                 image_right,
                 replace):
    url = f'{moodle}/webservice/rest/server.php'
    data = {
        'moodlewsrestformat': 'json',
        'wstoken': wstoken,
        'wsfunction': CREATE_IMAGE,
        'username': username,
        'image_front': image_front,
        'image_left': image_left,
        'image_right': image_right,
        'replace': replace
    }
    r = req.post(url, data=data)
    res = res_handle(r)

    if 'status' in res:
        raise ErrorAPI(res['status'], res['message'], 'moodle')
    return res


def get_image(moodle, wstoken, username):
    url = f'{moodle}/webservice/rest/server.php'
    params = {
        'moodlewsrestformat': 'json',
        'wstoken': wstoken,
        'wsfunction': GET_IMAGE,
        'username': username
    }
    r = req.post(url, params=params)
    res = res_handle(r)

    if not res:
        raise ErrorAPI(404, 'images not found', 'moodle')
    if 'status' in res:
        raise ErrorAPI(res['status'], res['message'], 'moodle')
    if isinstance(res, list):
        return res[0]
    return res


def verify(
        moodle,
        wstoken,
        username,
        sessionid,
        image_front,
        image_left,
        image_right,
        result):
    url = f'{moodle}/webservice/rest/server.php'
    data = {
        'moodlewsrestformat': 'json',
        'wstoken': wstoken,
        'wsfunction': CHECKIN_ONLINE,
        'username': username,
        'sessionid': sessionid,
        'image_front': image_front,
        'image_left': image_left,
        'image_right': image_right,
        'result': result
    }
    r = req.post(url, data=data)
    res = res_handle(r)

    if 'status' in res:
        raise ErrorAPI(res['status'], res['message'], 'moodle')
    return res


def get_campus(moodle, wstoken):
    url = f'{moodle}/webservice/rest/server.php'
    params = {
        'moodlewsrestformat': 'json',
        'wstoken': wstoken,
        'wsfunction': GET_CAMPUS,
    }
    r = req.get(url, params=params)
    res = res_handle(r)

    if 'status' in res:
        raise ErrorAPI(res['status'], res['message'], 'moodle')
