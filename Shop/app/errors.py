import logging as lg
from flask import jsonify


#  === === The library of errors === ===
def make_error_response(error):
    lg.info(error["text"])
    return jsonify(error), 400

OK = {"text" : "[OK]"}

JSON_1 = {"text" : "[JSON-1] Couldn't get json from request"}

PGNT_1 = {"text" : "[PGNT-1] Arguement 'page_size' must be in range from 1 to 50"}
PGNT_2 = {"text" : "[PGNT-2] Arguement 'page_size' must be integer"}
PGNT_3 = {"text" : "[PGNT-3] Arguement 'page' out of range"}

AUTH_0 = {"text" : "[AUTH-0] Not authorized"}
AUTH_1 = {"text" : "[AUTH-1] No json with login and password"}
AUTH_2L = {"text" : "[AUTH-2L] No login in json"}
AUTH_2P = {"text" : "[AUTH-2P] No password in json"}
AUTH_3 = {"text" : "[AUTH-3] There's no user with this login"}
AUTH_4 = {"text" : "[AUTH-4] There's already a user with this login"}
AUTH_5 = {"text" : "[AUTH-5] Password is incorrect"}

EAN_1 = {"text" : "[EAN-1] There's no 'ean' field in json"}
EAN_2 = {"text" : "[EAN-2] There's no item eith this ean"}
EAN_3 = {"text" : "[EAN-3] There's already an item with this ean"}


CREATE_1 = {"text" : "[CREATE-1] No 'itemname' in json"}


