from pymongo import MongoClient
from threading import Lock
import configparser
"""
class MongoDBConnection:
    config_file="config.ini"
    _instance = None
    _lock = Lock()

    def __new__(cls, uri, database_name, config_file = "../../config.ini"):
        if not cls._instance:
            print('new')

            _config = configparser.ConfigParser()
            _config.read(config_file)

            url=_config["database"]["MONGO_URL"]
            db=_config["database"]["DB_NAME"]

            print(url)
            print(db)

            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
                    cls._instance._client = MongoClient(uri)
                    cls._instance._db = cls._instance._client[database_name]
        return cls._instance

    def get_database(self):
        return self._db

    def get_client(self):
        return self._client


def get_db():
    db = MongoDBConnection('test', 't1')
    print('db')
    return db.get_database()

def get_client():
    db = MongoDBConnection('test', 't1')
    print('client')
    return db.get_client()



get_db()
get_db()
get_client()
get_db()
get_client()



import configparser
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from threading import Lock

#--

#---

CONFIG_FILE="config.ini"

class DBConnection:
    
    #db_client = None

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
            
"""