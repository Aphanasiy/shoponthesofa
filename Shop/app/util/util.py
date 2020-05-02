def marshall_item(item):
    return {
        "id": item[3],
        "itemname": item[0],
        "ean": item[1],
        "category": item[2],
    }