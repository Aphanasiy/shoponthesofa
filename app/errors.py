import logging as lg
from flask import jsonify

#  === === The library of errors === ===

def make_error_responce(error):
    lg.info(error["text"])
    return jsonify(error), 400 


JSON_1 = {"text" : "[JSON-1] Couldn't write json from request"}

EAN_1 = {"text" : "[EAN-1] There's no 'ean' field in json"}
EAN_2 = {"text" : "[EAN-2] There's no item eith this ean"}
EAN_3 = {"text" : "[EAN-3] There's already an item with this ean"}


CREATE_1 = {"text" : "[CREATE-1] No 'itemname' in json"}


