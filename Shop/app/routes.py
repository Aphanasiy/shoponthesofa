from app import *

from flask import jsonify
from flask import request
from flask import abort
from flask import make_response, url_for
import logging as lg


@app.route('/')
def index():
    return jsonify(message="Hello World!"), 200
