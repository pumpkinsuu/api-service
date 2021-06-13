import requests as req

from config import server

from utilities import logger, ErrorAPI
log = logger('face')


def users(api_key: str):
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


def exist(api_key: str, userID: str):
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


def create(api_key: str, user: dict):
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


def update(api_key: str, user: dict):
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


def remove(api_key: str, userID):
    headers = {
        'api_key': api_key
    }
    url = f'{server.FACE_URL}/users/{userID}'
    r = req.delete(url, headers=headers)

    res = r.json()
    if 'error' in res:
        err = res['error']
        raise ErrorAPI(err['code'], err['message'])


def find(api_key: str, images: list):
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

    return res


def verify(api_key: str, image1, image2):
    headers = {
        'api_key': api_key
    }
    url = f'{server.FACE_URL}/verify'
    data = {
        'image1': image1,
        'image2': image2
    }
    r = req.post(url, data=data, headers=headers)

    res = r.json()
    if 'error' in res:
        err = res['error']
        raise ErrorAPI(err['code'], err['message'])

    return res['result']


def count(api_key: str):
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
