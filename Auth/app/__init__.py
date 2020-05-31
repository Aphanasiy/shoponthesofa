# -*- coding: utf-8 -*-

from flask import Flask
from .config import Config

app = Flask(__name__)
app.config.from_object(Config)


from app.errors import *
from app import database
shdb = database.ShopDatabase()

from app import routes
