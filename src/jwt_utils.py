import datetime

import jwt

SECRET_KEY = "your-secret-key"


def generate_jwt(email):
    payload = {"email": email, "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)}
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def validate_jwt(token):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        exp_timestamp = decoded_token["exp"]

        exp_datetime = datetime.datetime.utcfromtimestamp(exp_timestamp)

        if exp_datetime >= datetime.datetime.utcnow():
            return decoded_token
        else:
            return False
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False
