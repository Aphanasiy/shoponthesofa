from app import *
from app import util
from app import db_util

from flask import jsonify
from flask import request
from flask import abort
from flask import make_response, url_for
import logging as lg


from passlib.hash import pbkdf2_sha512 as SHA512
import jwt



@app.route('/')
@util.parse_headers
def index(**kwagrs):
    return jsonify(message="Hello World!"), 200


@app.route('/register', methods=["POST"])
@util.parse_headers
def register(headers = None, **kwargs):
    print(headers)
    if "Login" not in headers:
        return make_error_response(AUTH_2L)
    if "Password" not in headers:
        return make_error_response(AUTH_2P)
    if "Email" not in headers:
        return make_error_response(AUTH_2E)
    hsh = SHA512.hash(headers['Password'])

    if (db_util.check_if_user_exists(headers["Login"])):
        print("EXISTS")
        return make_error_response(AUTH_4L)
    if (db_util.check_if_email_exists(headers["Email"])):
        return make_error_response(AUTH_4E)

    request = f"""INSERT INTO users.users(login, password, email) VALUES
    (
        '{headers["Login"].lower()}', '{hsh}', '~{headers["Email"].lower()}'
    )
    """
    shdb.execute(request, "Adding new user")
    return make_ok_response()


@app.route('/auth')
@util.parse_headers
def auth(headers = None, **kwargs):
    if "Login" not in headers:
        return make_error_response(AUTH_2L)
    if "Password" not in headers:
        return make_error_response(AUTH_2P)
    if (not db_util.check_if_user_exists(headers['Login'])):
        return make_error_response(AUTH_3)
    hsh = shdb.read(f"SELECT password FROM users.users WHERE login = '{headers['Login'].lower()}'")[0][0]
    if not SHA512.verify(headers["Password"], hsh):
        return make_error_response(AUTH_5)

    act, rft = db_util.make_tokens(headers["Login"])
    response = make_response(OK, 200)
    response.headers["Login"] = headers["Login"]
    response.headers["Access-Token"] = act
    response.headers["Refresh-Token"] = rft
    return response


@app.route('/change_password', methods=["PUT"])
@util.parse_headers
def change_password(headers = None,**kwargs):
    if "Login" not in headers:
        return make_error_response(AUTH_2L)
    if "Password" not in headers:
        return make_error_response(AUTH_2P)
    if "New-Password" not in headers:
        return make_error_response(AUTH_2NP)
    if (not db_util.check_if_user_exists(headers['Login'])):
        return make_error_response(AUTH_3)
    hsh = shdb.read(f"SELECT password FROM users.users WHERE login = '{headers['Login'].lower()}'")[0][0]
    if not SHA512.verify(headers["Password"], hsh):
        return make_error_response(AUTH_5)

    nhsh = SHA512.hash(headers["New-Password"])
    print(SHA512.verify(headers["Password"], hsh), SHA512.verify(headers["New-Password"], hsh))
    request = f"""UPDATE users.users SET password = '{nhsh}' WHERE login = '{headers["Login"].lower()}'"""
    print(request)
    make_tokens() #changing tokens first
    shdb.execute(request, "Changing password")
    return make_ok_response()


@app.route('/refresh', methods=['GET'])
@util.parse_headers
def refresh(headers=None, **kwargs):
    if ("Login" not in headers):
        return make_error_response(AUTH_2L)
    if ("Refresh-Token" not in headers):
        return make_error_response(AUTH_2RT)
    if (not db_util.check_if_user_exists(headers['Login'])):
        return make_error_response(AUTH_3)
    
    x = shdb.read(f"""SELECT EXISTS (
        SELECT * FROM users.tokens WHERE login = '{headers["Login"].lower()}' AND
                                         refresh_token = '{headers["Refresh-Token"]}'
    )""")[0][0]
    if (not x):
        return make_error_response(AUTH_5RT)
    is_fresh = shdb.read(f"""SELECT now() - (SELECT "Created" FROM users.tokens 
          WHERE login = '{headers["Login"].lower()}') < interval '1 hour';""")[0][0]
    if (not is_fresh):
        return make_error_response(AUTH_5RT)

    response = make_response()
    act, rft = db_util.make_tokens(headers["Login"])
    response.headers["Login"] = headers["Login"]
    response.headers["Access-Token"] = act
    response.headers["Refresh-Token"] = rft
    return response


@app.route('/access', methods=['GET'])
@util.parse_headers
def access(headers=None, **kwargs):
    if ("Login" not in headers):
        return make_error_response(AUTH_2L)
    if ("Access-Token" not in headers):
        return make_error_response(AUTH_2AT)
    if (not db_util.check_if_user_exists(headers['Login'])):
        return make_error_response(AUTH_3)
    
    x = shdb.read(f"""SELECT EXISTS (
        SELECT * FROM users.tokens WHERE login = '{headers["Login"].lower()}' AND
                                         access_token = '{headers["Access-Token"]}'
    )""")[0][0]
    if (not x):
        return make_error_response(AUTH_5A)
    is_fresh = shdb.read(f"""SELECT now() - (SELECT "Created" FROM users.tokens 
          WHERE login = '{headers["Login"].lower()}') < interval '5 minutes';""")[0][0]
    if (not is_fresh):
        return make_error_response(AUTH_5A)


    user_info = shdb.read(f"""SELECT email, "DistributorID", role FROM users.users WHERE login = '{headers["Login"].lower()}'""")
    print(user_info)
    json = {}
    json["email"] = user_info[0][0]
    json["distributorID"] = user_info[0][1]
    json["role"] = user_info[0][2]
    
    response = make_response(json, 200)

    response.headers["Login"] = headers["Login"]
    return response