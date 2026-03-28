import configparser
from pymongo import MongoClient
from pymongo.collection import Collection

config = configparser.ConfigParser()
config.read("config.ini")

MONGO_URL = config["database"]["MONGO_URL"]
DB_NAME = config["database"]["DB_NAME"]

client = MongoClient(MONGO_URL)

def get_mongo_client():
    return client

def get_db_conn(client: MongoClient) -> Collection:
    db = client[DB_NAME]
    return db

