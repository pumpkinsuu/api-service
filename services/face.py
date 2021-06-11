import requests as req

from config import server

from utilities import logger, ErrorAPI
log = logger('face')


def users(api_key: str):
    try:
        headers = {
            'api_key': api_key
        }
        url = f'{server.FACE_URL}/users'
        r = req.get(url, headers=headers)

        res = r.json()
        if 'error' in res:
            err = res['error']
            raise ErrorAPI(err['code'], err['message'])

        return res['users']
    except Exception as ex:
        log.info(str(ex), exc_info=True)
        raise ErrorAPI(500, str(ex))


def exist(api_key: str, userID: str):
    try:
        headers = {
            'api_key': api_key
        }
        url = f'{server.FACE_URL}/users/{userID}'
        r = req.get(url, headers=headers)

        res = r.json()
        if 'error' in res:
            err = res['error']
            raise ErrorAPI(err['code'], err['message'])

        return res['status']
    except Exception as ex:
        log.info(str(ex), exc_info=True)
        raise ErrorAPI(500, str(ex))


def create(api_key: str, user: dict):
    try:
        headers = {
            'api_key': api_key
        }
        url = f'{server.FACE_URL}/users/{user["id"]}'
        r = req.post(url, data=user, headers=headers)

        res = r.json()
        if 'error' in res:
            err = res['error']
            raise ErrorAPI(err['code'], err['message'])

        return res
    except Exception as ex:
        log.info(str(ex), exc_info=True)
        raise ErrorAPI(500, str(ex))


def update(api_key: str, user: dict):
    try:
        headers = {
            'api_key': api_key
        }
        url = f'{server.FACE_URL}/users/{user["id"]}'
        r = req.put(url, data=user, headers=headers)

        res = r.json()
        if 'error' in res:
            err = res['error']
            raise ErrorAPI(err['code'], err['message'])

        return res
    except Exception as ex:
        log.info(str(ex), exc_info=True)
        raise ErrorAPI(500, str(ex))


def remove(api_key: str, userID):
    try:
        headers = {
            'api_key': api_key
        }
        url = f'{server.FACE_URL}/users/{userID}'
        r = req.delete(url, headers=headers)

        res = r.json()
        if 'error' in res:
            err = res['error']
            raise ErrorAPI(err['code'], err['message'])

        return res['status']
    except Exception as ex:
        log.info(str(ex), exc_info=True)
        raise ErrorAPI(500, str(ex))


def find(api_key: str, images: list):
    try:
        headers = {
            'api_key': api_key
        }
        url = f'{server.FACE_URL}/find'
        data = {
            'images': images
        }
        r = req.post(url, data=data, headers=headers)

        res = r.json()
        if 'error' in res:
            err = res['error']
            raise ErrorAPI(err['code'], err['message'])

        return r.json()
    except Exception as ex:
        log.info(str(ex), exc_info=True)
        raise ErrorAPI(500, str(ex))


def count(api_key: str):
    try:
        headers = {
            'api_key': api_key
        }
        url = f'{server.FACE_URL}/count'
        r = req.get(url, headers=headers)

        res = r.json()
        if 'error' in res:
            err = res['error']
            raise ErrorAPI(err['code'], err['message'])

        return res['total']
    except Exception as ex:
        log.info(str(ex), exc_info=True)
        raise ErrorAPI(500, str(ex))
