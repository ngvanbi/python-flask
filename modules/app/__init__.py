import datetime
import json
import os

from bson.objectid import ObjectId
from flask import Flask
from flask_pymongo import PyMongo

from app.controllers import *


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

# Add mongo URL to flask config, so that flask_pymongo can use it to make connection
app.config['MONGO_URI'] = os.environ.get('DB')
mongo = PyMongo(app)

# Use the modified encoder class to handle ObjectId and datetime object while jsonifying the response.
app.json_encoder = JSONEncoder
