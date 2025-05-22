import jwt
from datetime import datetime, timedelta
from django.conf import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = 'HS256'
EXPIRE_MINUTES = 60

def generate_jwt(user):
    payload = {
        'user_id': user.id,
        'username': user.username,
        'exp': datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTES)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_jwt(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None

def decode_jwt(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
