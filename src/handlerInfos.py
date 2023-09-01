from flask import jsonify

from src.dynamodb_manager import dynamodb_client

USERS_TABLE = 'InfoTable'


def save_info(email, name, address, phone):
    try:
        dynamodb_client.put_item(
            TableName=USERS_TABLE,
            Item={
                'email': {'S': email},
                'name': {'S': name},
                'address': {'S': address},
                'phone': {'S': phone}
            }
        )
        return jsonify({'message': 'Information saved successfully'}), 200
    except Exception as e:
        return jsonify({'error': 'An error occurred while saving information'}), 500
