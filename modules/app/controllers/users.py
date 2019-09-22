import os

from flask import jsonify, request
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required,
                                get_jwt_identity)
import logger
from app import app, mongo, flask_bcrypt, jwt
from app.schemas import validate_user

ROOT_PATH = os.environ.get('ROOT_PATH')
LOG = logger.get_root_logger(
    __name__, filename=os.path.join(ROOT_PATH, 'output.log')
)


@app.route("/auth", methods=['POST'])
def auth_user():
    """Auth endpoint."""
    data = validate_user(request.get_json())
    if data.get('ok'):
        data = data.get('data')
        user_data = mongo.db.users.find_one({'email': data.get('email')}, {'_id': 0})
        LOG.debug(user_data)
        if user_data and flask_bcrypt.check_password_hash(user_data.get('password'), data.get('password')):
            del user_data['password']
            access_token = create_access_token(identity=data)
            refresh_token = create_refresh_token(identity=data)
            user_data['token'] = access_token
            user_data['refresh'] = refresh_token
            return jsonify({'ok': True, 'data': user_data}), 200
        else:
            return jsonify({'ok': False, 'message': 'Invalid username or password'}), 401
    else:
        return jsonify({'ok': False, 'message': 'Bad request parameters: {}'.format(data.get('message'))}), 400


@app.route('/register', methods=['POST'])
def register():
    """Register use endpoint."""
    data = validate_user(request.get_json())
    if data['ok']:
        data = data['data']
        data['password'] = flask_bcrypt.generate_password_hash(data['password'])
        mongo.db.users.insert_one(data)
        return jsonify({'ok': True, 'message': 'User created successfully!'}), 200
    else:
        return jsonify({'ok': True, 'message': 'Base request parameters:{}'.format(data['message'])}), 400


@app.route('/user', methods=['GET', 'POST', 'DELETE', 'PATCH'])
def user():
    if request.method == 'GET':
        query = request.args
        data = mongo.db.users.find_one(query)
        return jsonify(data), 200

    data = request.get_json()
    if request.method == 'POST':
        if data.get('name', None) is not None and data.get('email', None) is not None:
            mongo.db.users.insert_one(data)
            return jsonify({'ok': True, 'message': 'User created successfully!'}), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400

    if request.method == 'DELETE':
        if data.get('email', None) is not None:
            db_response = mongo.db.users.delete_one({'email': data['email']})
            if db_response.deleted_count == 1:
                response = {'ok': True, 'message': 'record deleted'}
            else:
                response = {'ok': True, 'message': 'no record found'}
            return jsonify(response), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400

    if request.method == 'PATCH':
        if data.get('query', {}) != {}:
            mongo.db.users.update_one(
                data['query'], {'$set': data.get('payload', {})}
            )
            return jsonify({'ok': True, 'message': 'record updated'}), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400
