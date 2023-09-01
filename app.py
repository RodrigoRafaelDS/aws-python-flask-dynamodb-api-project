from flask import Flask, jsonify, make_response, request

from src.handlerInfos import save_info
from src.handlerUser import create_user, validate_login
from src.jwt_utils import validate_jwt
from src.validations import is_valid_email, is_strong_password

app = Flask(__name__)


@app.route('/saveUser', methods=['POST'])
def save_user():
    email = request.json.get('email')
    password = request.json.get('password')

    if not is_valid_email(email):
        return jsonify({'error': 'Please provide a valid email and password'}), 400

    if not is_strong_password(password):
        return jsonify({'error': 'Please provide a valid password'}), 400

    return create_user(email, password)


@app.route('/login', methods=['GET'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    if not is_valid_email(email):
        return jsonify({'error': 'Please provide a valid email and password'}), 400

    if not is_strong_password(password):
        return jsonify({'error': 'Please provide a valid password'}), 400

    return validate_login(email, password)


@app.route('/saveInfo', methods=['POST'])
def save_info_endpoint():
    data = request.json
    auth_header = request.headers.get('Authorization')

    email = data.get('email')
    name = data.get('name')
    address = data.get('address')
    phone = data.get('phone')

    if not email or not name or not address or not phone:
        return jsonify({'error': 'Please provide all required fields'}), 400

    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Authorization required'}), 401

    token = auth_header.split(' ')[1]
    decoded_token = validate_jwt(token)

    if not decoded_token or 'email' not in decoded_token:
        return jsonify({'error': 'Invalid token'}), 401

    token_email = decoded_token['email']

    if not token_email or token_email != email:
        return jsonify({'error': 'Invalid token (email)'}), 401

    result = save_info(email, name, address, phone)
    return result


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)
