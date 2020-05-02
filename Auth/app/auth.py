from app import *
from flask import request, make_response, url_for
import hashlib


# hasher = hashlib.sha512()

def cipher(password):
    # hasher.update((password[0::2] + password + password[1::2]).encode("UTF-8"))
    # return hasher.hexdigest()
    return password[0::2] + password + password[1::2]


@app.route('/auth', methods=['GET'])
def auth():
    if not request.json:
        return make_error_response(AUTH_1)
    if "login" not in request.json:
        return make_error_response(AUTH_2L)
    if "password" not in request.json:
        return make_error_response(AUTH_2P)
    login = request.json["login"]
    print(request.json["password"])
    password = cipher(request.json["password"])
    x = shdb.read("SELECT password FROM Users.Users WHERE \"login\" = '{}'".format(login))
    if (len(x) == 0):
        return make_error_response(AUTH_3)
    print(password, x[0][0])
    if (password != x[0][0]):
        return make_error_response(AUTH_5)
    else:
        res_login = make_response()
        res_login.set_cookie("login", login, max_age=60 * 60 * 24 * 7 * 4)
        res_login.headers['location'] = url_for('auth')
        return jsonify(error="OK"), 200


@app.route('/register', methods=['POST'])
def register():
    if not request.json:
        return make_error_response(AUTH_1)
    if "login" not in request.json:
        return make_error_response(AUTH_2L)
    if "password" not in request.json:
        return make_error_response(AUTH_2P)
    login = request.json["login"]
    print(request.json["password"])
    password = cipher(request.json["password"])
    x = shdb.read("SELECT password FROM Users.Users WHERE \"login\" = '{}'".format(login))
    print(x)
    if (len(x) != 0):
        return make_error_response(AUTH_4)
    else:
        print(cipher(password))
        x = shdb.execute("INSERT INTO Users.Users VALUES ('{}', '{}')".format(login, password))

        res_login = make_response()
        return jsonify(error="OK"), 200


@app.route('/logout', methods=['GET'])
def logout():
    res_login = make_response()
    login = request.json["login"]
    res_login.set_cookie("login", login, max_age=0)
    res_login.headers['location'] = url_for('/')
    return jsonify(error="OK"), 200


"""
   curl -X GET localhost:5000/auth
   curl -X GET -H "Content-Type: application/json" -d "{\"ean\": 202, \"itemname\": \"Пуговица\"}" http://localhost:5000/auth
   curl -X GET -H "Content-Type: application/json" -d "{\"login\": \"aphanasiy\"}" http://localhost:5000/auth
   curl -X GET -H "Content-Type: application/json" -d "{\"login\": \"aphanasiy\", \"password\": \"abacaba\"}" http://localhost:5000/auth
   curl -X POST -H "Content-Type: application/json" -d "{\"login\": \"aphanasiy\", \"password\": \"abacaba\"}" http://localhost:5000/register
   curl -X GET -H "Content-Type: application/json" -d "{\"login\": \"aphanasiy\", \"password\": \"abacaba\"}" http://localhost:5000/auth

"""
