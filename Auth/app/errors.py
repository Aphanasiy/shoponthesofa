import logging as lg
from flask import jsonify


#  === === The library of errors === ===
def make_error_response(error):
    lg.info(error["text"])
    return jsonify(error), 400


def make_ok_response():
    lg.info(OK)
    return jsonify(OK), 200

OK = {"text" : "[OK]"}

JSON_1 = {"text" : "[JSON-1] Couldn't get json from request"}

AUTH_0 = {"text" : "[AUTH-0] Not authorized"}
AUTH_1 = {"text" : "[AUTH-1] No json with login and password"}
AUTH_2L = {"text" : "[AUTH-2L] No login in headers"}
AUTH_2P = {"text" : "[AUTH-2P] No password in headers"}
AUTH_2E = {"text" : "[AUTH-2E] No email in headers"}
AUTH_2AT = {"text" : "[AUTH-2AT] No refresh token in headers"}
AUTH_2RT = {"text" : "[AUTH-2RT] No refresh token in headers"}
AUTH_2NP = {"text" : "[AUTH-2NP] No new password in headers"}


AUTH_3 = {"text" : "[AUTH-3] There's no user with this login"}
AUTH_4L = {"text" : "[AUTH-4L] There's already a user with this login"}
AUTH_4E = {"text" : "[AUTH-4E] There's already a user with this email"}
AUTH_5 = {"text" : "[AUTH-5] Invalid password"}
AUTH_5A = {"text" : "[AUTH-5A] Invalid access token"}
AUTH_5RT = {"text" : "[AUTH-5RT] Invalid refresh token"}


