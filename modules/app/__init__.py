import datetime
import json
import os

from bson.objectid import ObjectId
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo


class JSONEncoder(json.JSONEncoder):
    """Extend json-encoder class"""

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return str(o)

        return json.JSONEncoder.default(self, o)


# Create the flask object
app = Flask(__name__)
app.config['MONGO_URI'] = os.environ.get('DB')
app.config['JWT_SECRET_KEY'] = os.environ.get('SECRET')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)

mongo = PyMongo(app)
flask_bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Use the modified encoder class to handle ObjectId and datetime object while jsonifying the response.
app.json_encoder = JSONEncoder

from app.controllers import *
