import configparser
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection

#--
"""
config = configparser.ConfigParser()
config.read("config.ini")

MONGO_URL = config["database"]["MONGO_URL"]
DB_NAME = config["database"]["DB_NAME"]

client = MongoClient(MONGO_URL)

def get_mongo_client():
    return client

def get_db_conn(client: MongoClient) -> Database:
    db = client[DB_NAME]
    return db
"""
#---

CONFIG_FILE="config.ini"

class DBConnection:
    def __init__(self, client: MongoClient = None, config_file: str = CONFIG_FILE):
        self._config = configparser.ConfigParser()
        self._config.read(config_file)
        
        try:
            self.db_url = self._config["database"]["MONGO_URL"]
            self.db_name = self._config["database"]["DB_NAME"]
        except Exception as e:
            print(e)
            raise MongoConfigError(f"Missing configurations {e}")
        
        if client is None:
            self._client: MongoClient | None = None
        else:
            self._client = client

    def get_client(self) -> MongoClient:
        if self._client is None:
            try:
                print("New client!")
                self._client = MongoClient(self.db_url)
            except PyMongoError as e:
                print(e)
                raise RuntimeError(f"Failed to connect to DB: {e}")
        return self._client

    def get_db(self) -> Database:
        client = self.get_client()
        return client[self.db_name]

    def get_collection(self, collection_name: str) -> Collection:
        db = self.get_db()
        collection = db[collection_name]
        return collection

    def close(self):
        if self._client:
            self._client.close()
            self._client = None
            