import json
from pymongo import MongoClient
from pymongo.collection import Collection

MONGO_URL = "mongodb://localhost:27017/"
DB_NAME = "order_db"
COLLECTION_NAME = "user"

def __get_db_conn() -> Collection:
    client = MongoClient(MONGO_URL)
    db = client[DB_NAME]
    col = db[COLLECTION_NAME]
    return col

def __id_serialiser(object)-> dict:
    #object["id"] = str(object["_id"])
    del object["_id"]
    return object

def create_user(email: str, name: str):
    mycol = __get_db_conn()
    mycol.insert_one({"email": email, "name": name})

def validate_user(email) -> str:
    mycol = __get_db_conn()
    user = mycol.find_one({"email": email})

    if user != None and len(user['email']) != 0:
        return user['email']
    else: 
        return None

def get_user(email) -> str:
    mycol = __get_db_conn()
    user = mycol.find_one({"email": email})

    if user != None and len(user['email']) != 0:
        return __id_serialiser(user)
    else: 
        return None
