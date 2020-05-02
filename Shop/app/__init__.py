# -*- coding: utf-8 -*-

from flask import Flask
from .config import Config
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

from app.errors import *
from app import database
shdb = database.ShopDatabase()

from app import routes
from app import api