# -*- coding: utf-8 -*-

from app import *
from flask import jsonify
from flask import request
from flask import abort

import logging as lg

def marshall_item(item):
    return {
        "id": item[3],
        "itemname": item[0],
        "ean": item[1],
        "category": item[2],
    }

@app.route('/')
def index():
    return jsonify(message="Hello World!"), 200


@app.route('/api/v1.0/create_item', methods=['POST'])
def create_item():
    if (not request.json):
        return make_error_responce(JSON_1)
    if (not 'itemname' in request.json):
        return make_error_responce(CREATE_1)
    if (not 'ean' in request.json):
        return make_error_responce(EAN_1)

    ItemName = request.json["itemname"]
    EAN = request.json["ean"]
    Category = "'{}'".format(request.json["category"]) \
                          if "category" in request.json else ""
    if (len(shdb.read("SELECT * FROM Items.ItemInfo WHERE \"EAN\" = {}".format(EAN))) > 0):
        return make_error_responce(EAN_3)
    query = "INSERT INTO Items.ItemInfo" \
                              " VALUES ('{}', {}, {}) ".format(ItemName, EAN, Category)
    shdb.execute(query, "create_item ({}, {})".format(ItemName, EAN))
    return jsonify(error="OK"), 200

"""
aphanasiy@aphanasiylaptop:~/Documents/HSE/Trash$ 
curl -X POST -H "Content-Type: application/json" -d "{"ean": 202", "itemname": "Пуговица" http://localhost:5000/api/v1.0/create_item
curl -X DELETE -H "Content-Type: application/json" -d "@data.json" http://localhost:5000/api/v1.0/delete_item

"""

@app.route('/api/v1.0/delete_item', methods=['DELETE'])
def delete_item():
    if (not request.json):
        return make_error_responce(JSON_1)
    if (not 'ean' in request.json):
        return make_error_responce(EAN_1)
    EAN = request.json["ean"]
    if (len(shdb.read("SELECT * FROM Items.ItemInfo WHERE \"EAN\" = {}".format(EAN))) == 0):
        return make_error_responce(EAN_2)
    return jsonify(error="OK"), 200

@app.route('/api/v1.0/get_items', methods=['GET'])
def get_items():
    if (not request.json):
        return make_error_responce(JSON_1)
    items = shdb.read("SELECT * FROM Items.ItemInfo")
    return jsonify([marshall_item(x) for x in items]), 200

@app.route('/api/v1.0/get_item', methods=['GET'])
def get_item():
    if (not request.json):
        return make_error_responce(JSON_1)
    if (not 'ean' in request.json):
        return make_error_responce(EAN_1)
    EAN = request.json["ean"]
    x = shdb.read("SELECT * FROM Items.ItemInfo WHERE \"EAN\" = {}".format(EAN))
    if (len(x) == 0):
        return make_error_responce(EAN_2)
    return jsonify(marshall_item(x[0])), 200

@app.route('/api/v1.0/edit_item', methods=['PUT'])
def edit_item():
    if (not request.json):
        return make_error_responce(JSON_1)
    if (not 'ean' in request.json):
        return make_error_responce(EAN_1)
    EAN = request.json["ean"]
    if (len(shdb.read("SELECT * FROM Items.ItemInfo WHERE \"EAN\" = {}".format(EAN))) == 0):
        return make_error_responce(EAN_2)
    
    x = marshall_item(shdb.read("SELECT * FROM Items.ItemInfo WHERE \"EAN\" = {}".format(EAN))[0])

    ItemName = request.json["itemname"] if "itemname" in request.json else x["itemname"]
    Category = "'{}'".format(
               request.json["category"] if "category" in request.json else x["category"]
               )
    shdb.execute("UPDATE Items.ItemInfo "
                    "SET \"ItemName\" = '{}'".format(ItemName) + ", "
                        "Category = {}".format(Category) + " "
                        "WHERE \"EAN\" = {}".format(EAN)
                )
    return jsonify(error="OK"), 200