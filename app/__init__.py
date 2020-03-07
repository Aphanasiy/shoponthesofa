# -*- coding: utf-8 -*-

from flask import Flask
from app.errors import *
from app import database

app = Flask(__name__)

shdb = database.ShopDatabase()

from app import routes

