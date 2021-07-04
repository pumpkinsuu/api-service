# Server
HOST = '0.0.0.0'
PORT = 5000
# Face service
FACE_URL = 'http://localhost:5001'
# Mongo
MONGO_URI = "mongodb+srv://admin:AdminPass123@cluster0.zfker.mongodb.net/"
KEY_DB = 'key_db'
# User routes
USER_ROUTES = [
    '/face/users',
    '/face/users/verify',
    '/api/schedules'
]
