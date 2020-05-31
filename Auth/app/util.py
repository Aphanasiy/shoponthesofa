from app import *

from flask import jsonify
from flask import request
from flask import abort
from flask import make_response, url_for
import logging as lg


def parse_headers(handler):
    def f(*args, **kwargs):
        return handler(headers = dict(request.headers), *args, **kwargs)
    f.__name__ = handler.__name__
    return f


