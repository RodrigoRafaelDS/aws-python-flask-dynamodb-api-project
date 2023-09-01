import jwt
import datetime

SECRET_KEY = "your-secret-key"


def generate_jwt(email):
    payload = {
        'email': email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token


def validate_jwt(token):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return decoded_token if decoded_token['exp'] >= datetime.datetime.utcnow() else False
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False
