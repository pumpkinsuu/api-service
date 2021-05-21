import requests as req

import config

from utilities import logger, ErrorAPI
log = logger('face')


def users(collection: str):
    try:
        url = f'{config.FACE_URL}/{collection}/users'
        r = req.get(url)
        return r.json()
    except Exception as ex:
        log.info(str(ex), exc_info=True)
        raise ErrorAPI(500, 'something wrong')


def exist(collection: str, userID: str):
    try:
        url = f'{config.FACE_URL}/{collection}/users/{userID}'
        r = req.get(url)
        return r.json()
    except Exception as ex:
        log.info(str(ex), exc_info=True)
        raise ErrorAPI(500, 'something wrong')


def create(collection: str, user: dict):
    try:
        url = f'{config.FACE_URL}/{collection}/users/{user["id"]}'
        r = req.post(url, data=user)
        return r.json()
    except Exception as ex:
        log.info(str(ex), exc_info=True)
        raise ErrorAPI(500, 'something wrong')


def update(collection: str, user: dict):
    try:
        url = f'{config.FACE_URL}/{collection}/users/{user["id"]}'
        r = req.put(url, data=user)
        return r.json()
    except Exception as ex:
        log.info(str(ex), exc_info=True)
        raise ErrorAPI(500, 'something wrong')


def remove(collection: str, userID):
    try:
        url = f'{config.FACE_URL}/{collection}/users/{userID}'
        r = req.delete(url)
        return r.json()
    except Exception as ex:
        log.info(str(ex), exc_info=True)
        raise ErrorAPI(500, 'something wrong')


def find(collection: str, images: list):
    try:
        url = f'{config.FACE_URL}/{collection}/find'
        data = {
            'images': images
        }
        r = req.post(url, data=data)
        return r.json()
    except Exception as ex:
        log.info(str(ex), exc_info=True)
        raise ErrorAPI(500, 'something wrong')


def count(collection: str):
    try:
        url = f'{config.FACE_URL}/{collection}'
        r = req.get(url)
        return r.json()
    except Exception as ex:
        log.info(str(ex), exc_info=True)
        raise ErrorAPI(500, 'something wrong')


def rename(collection: str, name: str):
    try:
        url = f'{config.FACE_URL}/{collection}'
        json = {'name': name}
        r = req.put(url, json=json)
        return r.json()
    except Exception as ex:
        log.info(str(ex), exc_info=True)
        raise ErrorAPI(500, 'something wrong')


def drop(collection: str):
    try:
        url = f'{config.FACE_URL}/{collection}'
        r = req.delete(url)
        return r.json()
    except Exception as ex:
        log.info(str(ex), exc_info=True)
        raise ErrorAPI(500, 'something wrong')
