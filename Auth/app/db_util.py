from app import *
from app import util

from flask import jsonify
from flask import request
from flask import abort
from flask import make_response, url_for
import logging as lg


from passlib.hash import pbkdf2_sha512 as SHA512
import secrets

def check_if_user_exists(login):
    query = f"""SELECT EXISTS (
        SELECT * FROM Users.users WHERE login = '{login.lower()}'
               );"""
    return shdb.read(query)[0][0]

def check_if_email_exists(email):
    query = f"""SELECT EXISTS (
    SELECT * FROM Users.users WHERE email SIMILAR TO '(~)?{email.lower()}'
           );"""
    return shdb.read(query)[0][0]

def make_tokens(login):
    access_token = secrets.token_hex(64)
    refresh_token = secrets.token_hex(64)
    query = f"""
     INSERT INTO users.tokens VALUES('{login.lower()}', '{access_token}', '{refresh_token}')
         ON CONFLICT(login) DO UPDATE 
        SET access_token='{access_token}', refresh_token='{refresh_token}', "Created" = CURRENT_TIMESTAMP;
    """
    shdb.execute(query)
    return access_token, refresh_token


