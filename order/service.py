import json
from pymongo import MongoClient
from pymongo.collection import Collection

MONGO_URL = "mongodb://localhost:27017/"
DB_NAME = "order_db"
COLLECTION_NAME = "order"

def __get_db_conn() -> Collection:
    client = MongoClient(MONGO_URL)
    db = client[DB_NAME]
    col = db[COLLECTION_NAME]
    return col

def __id_serialiser(object)-> dict:
    #object["id"] = str(object["_id"])
    del object["_id"]
    return object

def create_order(order_number: str, product: dict, user: str):
    order_col = __get_db_conn()
    #validate dict
    isinstance(product, dict)
    #lock product, 
    
    #reduce product stock
    order = order_col.insert_one({"order_number": order_number, "product": product, "user": user})

def get_order(order_number: str):
    order_col = __get_db_conn()
    order = order_col.find_one({"order_number": order_number})
    
    if order != None:
        return __id_serialiser(order)
    else:
        return None
