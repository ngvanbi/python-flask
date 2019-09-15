""""index file fro REST API using FLASK"""
import os
import sys

import requests
from flask import jsonify, make_response, request, send_from_directory

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
os.environ.update({'ROOT_PATH': ROOT_PATH})
sys.path.append(os.path.join(ROOT_PATH, 'modules'))

# PUBLIC_PATH = os.path.join(ROOT_PATH, 'public')

import logger  # noqa
from app import app  # noqa

# Create a logger object to log the info and debug
LOG = logger.get_root_logger(os.environ.get(
    'ROOT_LOGGER', 'root'), filename=os.path.join(ROOT_PATH, 'output.log'))

# Port variable to run the server on.
PORT = os.environ.get('PORT')


@app.errorhandler(404)
def not_found(error):
    LOG.error(error)
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/')
def index():
    return send_from_directory('dist', 'index.html')


@app.route('/<path:path>')
def static_proxy(path):
    """Static folder serve"""
    file_name = path.split('/')[-1]
    dir_name = os.path.join('dist', '/'.join(path.split('/')[:-1]))
    return send_from_directory(dir_name, file_name)


if __name__ == '__main__':
    LOG.info('Running environment: %s', os.environ.get('ENV'))
    app.config['DEBUG'] = os.environ.get('ENV') == 'development'  # Debug mode if development environment
    app.run(host='0.0.0.0', port=int(PORT))  # Run the app
