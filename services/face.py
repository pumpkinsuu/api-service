import requests as req

from config import server

from utilities import ErrorAPI


def users(Authorization: str):
    headers = {
        'Authorization': Authorization
    }
    url = f'{server.FACE_URL}/users'
    r = req.get(url, headers=headers)

    res = r.json()
    if 'error' in res:
        err = res['error']
        raise ErrorAPI(err['code'], err['message'], 'face')

    return res['users']


def exist(Authorization: str, userID: str):
    headers = {
        'Authorization': Authorization
    }
    url = f'{server.FACE_URL}/users/{userID}'
    r = req.get(url, headers=headers)

    res = r.json()
    if 'error' in res:
        err = res['error']
        raise ErrorAPI(err['code'], err['message'], 'face')

    return res['status']


def create(Authorization: str, user: dict):
    headers = {
        'Authorization': Authorization
    }
    url = f'{server.FACE_URL}/users/{user["id"]}'
    r = req.post(url, data=user, headers=headers)

    res = r.json()
    if 'error' in res:
        err = res['error']
        raise ErrorAPI(err['code'], err['message'], 'face')

    return res


def update(Authorization: str, user: dict):
    headers = {
        'Authorization': Authorization
    }
    url = f'{server.FACE_URL}/users/{user["id"]}'
    r = req.put(url, data=user, headers=headers)

    res = r.json()
    if 'error' in res:
        err = res['error']
        raise ErrorAPI(err['code'], err['message'], 'face')

    return res


def remove(Authorization: str, userID):
    headers = {
        'Authorization': Authorization
    }
    url = f'{server.FACE_URL}/users/{userID}'
    r = req.delete(url, headers=headers)

    res = r.json()
    if 'error' in res:
        err = res['error']
        raise ErrorAPI(err['code'], err['message'], 'face')


def find(Authorization: str, images: list):
    headers = {
        'Authorization': Authorization
    }
    url = f'{server.FACE_URL}/find'
    data = {
        'images': images
    }
    r = req.post(url, data=data, headers=headers)

    res = r.json()
    if 'error' in res:
        err = res['error']
        raise ErrorAPI(err['code'], err['message'], 'face')

    return res


def verify(Authorization: str, userID, images):
    headers = {
        'Authorization': Authorization
    }
    url = f'{server.FACE_URL}/verify'
    data = {
        'userID': userID,
        'images': images
    }
    r = req.post(url, data=data, headers=headers)

    res = r.json()
    if 'error' in res:
        err = res['error']
        raise ErrorAPI(err['code'], err['message'], 'face')

    return res['result']


def count(Authorization: str):
    headers = {
        'Authorization': Authorization
    }
    url = f'{server.FACE_URL}/count'
    r = req.get(url, headers=headers)

    res = r.json()
    if 'error' in res:
        err = res['error']
        raise ErrorAPI(err['code'], err['message'], 'face')

    return res['total']
