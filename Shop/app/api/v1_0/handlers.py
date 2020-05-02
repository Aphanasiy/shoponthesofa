# -*- coding: utf-8 -*-

from app import *

from app.util.util import marshall_item

from flask import jsonify
from flask import request
from flask import abort
from flask import make_response, url_for
import logging as lg


API_VERSION = "1.0"

@app.route(f'/api/v{API_VERSION}/item', methods=['POST'])
def create_item_1_0():
    if not request.json:
        return make_error_response(JSON_1)
    if 'itemname' not in request.json:
        return make_error_response(CREATE_1)
    if 'ean' not in request.json:
        return make_error_response(EAN_1)

    ItemName = request.json["itemname"]
    EAN = request.json["ean"]
    Category = "'{}'".format(request.json["category"]) \
        if "category" in request.json else ""
    if len(shdb.read("SELECT * FROM Items.ItemInfo WHERE \"EAN\" = {}".format(EAN))) > 0:
        return make_error_response(EAN_3)
    query = "INSERT INTO Items.ItemInfo" \
            " VALUES ('{}', {}, {}) ".format(ItemName, EAN, Category)
    shdb.execute(query, "create_item ({}, {})".format(ItemName, EAN))
    return jsonify(), 200


@app.route(f'/api/v{API_VERSION}/item', methods=['DELETE'])
def delete_item_1_0():
    if not request.json:
        return make_error_response(JSON_1)
    if 'ean' not in request.json:
        return make_error_response(EAN_1)
    EAN = request.json["ean"]
    shdb.execute("DELETE FROM Items.ItemInfo WHERE \"EAN\" = {}".format(EAN))
    return jsonify(), 200


@app.route(f'/api/v{API_VERSION}/items', methods=['GET'])
def get_items_1_0():
    count = shdb.read("SELECT COUNT(*) FROM Items.ItemInfo")[0][0]
    
    if not request.json:
        return make_error_response(JSON_1)
    if 'pageSize' not in request.json:
        return make_error_response(PGNT_1)
    page_size = request.json["pageSize"]
    if not (1 <= page_size <= 50):
        return make_error_response(PGNT_1)
    
    if 'page' not in request.json:
        return make_error_response(PGNT_2)
    page = request.json["page"] - 1
    if not (0 <= page < -(-count // page_size)):
        resp_json = {"pages": -(-count // page_size)}
        resp_json.update(PGNT_3)
        return make_error_response(resp_json)

    items = shdb.read("SELECT * FROM Items.ItemInfo ORDER BY \"EAN\"" +
                    f" OFFSET {page * page_size} LIMIT {page_size}")
    
    items_page = [marshall_item(x) for x in items]
    return jsonify({
        "items": items_page,
        "pages": -(-count // page_size)
                    }), 200


@app.route(f'/api/v{API_VERSION}/item', methods=['GET'])
def get_item_1_0():
    if not request.json:
        return make_error_response(JSON_1)
    if not 'ean' in request.json:
        return make_error_response(EAN_1)
    EAN = request.json["ean"]
    x = shdb.read("SELECT * FROM Items.ItemInfo WHERE \"EAN\" = {}".format(EAN))
    if len(x) == 0:
        return make_error_response(EAN_2)
    return jsonify(marshall_item(x[0])), 200


@app.route(f'/api/v{API_VERSION}/item', methods=['PUT'])
def edit_item_1_0():
    if not request.json:
        return make_error_response(JSON_1)
    if not 'ean' in request.json:
        return make_error_response(EAN_1)
    EAN = request.json["ean"]
    if len(shdb.read("SELECT * FROM Items.ItemInfo WHERE \"EAN\" = {}".format(EAN))) == 0:
        return make_error_response(EAN_2)

    x = marshall_item(shdb.read("SELECT * FROM Items.ItemInfo WHERE \"EAN\" = {}".format(EAN))[0])

    ItemName = request.json["itemname"] if "itemname" in request.json else x["itemname"]
    Category = "'{}'".format(
        request.json["category"] if "category" in request.json else x["category"]
    )
    shdb.execute(
                 "UPDATE Items.ItemInfo "
                 "SET \"ItemName\" = '{}'".format(ItemName) + ", "
                 "Category = {}".format(Category) + " "
                 "WHERE \"EAN\" = {}".format(EAN)
                )
    return jsonify(), 200
