from moodle_config import DEF_ROLE, ADMIN_ROLE
from config import API_KEY

import services.moodle as moodle
from utilities import ErrorAPI


def verify(args, admin=False):
    if 'token' not in args:
        raise ErrorAPI(400, 'missing "token"')

    if args['token'] == API_KEY:
        return

    role = DEF_ROLE
    if admin:
        role = ADMIN_ROLE

    result = moodle.token_info(args['token'])
    if not result:
        raise ErrorAPI(401, 'unauthorized request')

    user = moodle.user_info(result['username'])
    if not user or user['roleid'] not in role:
        raise ErrorAPI(401, 'no permission')
