from flask import jsonify
import hashlib
import secrets


from dynamodb_manager import dynamodb_client
from src.jwt_utils import generate_jwt

USERS_TABLE = 'users'

DEFAULT_SALT = secrets.token_hex(16)


def hash_password(password, salt=DEFAULT_SALT):
    hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()

    return hashed_password, salt


def create_user(email, password):
    hashed_password, salt = hash_password(password)

    dynamodb_client.put_item(
        TableName=USERS_TABLE, Item={'email': {'S': email}, 'password': {'S': hashed_password}, 'salt': {'S': salt}}
    )

    return jsonify({'email': email})


def validate_login(email, password):
    response = dynamodb_client.get_item(
        TableName=USERS_TABLE, Key={'email': {'S': email}}
    )

    if 'Item' not in response:
        return jsonify({'error': 'User not exist'}), 401

    user_item = response['Item']
    hashed_password = user_item['password']['S']
    salt = user_item['salt']['S']

    input_hashed_password, _ = hash_password(password, salt)

    if hashed_password == input_hashed_password:
        token = generate_jwt(email)
        return jsonify({'message': 'Login successful', 'token': token})

    return jsonify(
        {'error': 'Invalid username or password'}), 401
