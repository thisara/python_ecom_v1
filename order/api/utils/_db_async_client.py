import configparser
from motor.motor_asyncio import AsyncIOMotorClient
from threading import Lock
from api.utils.app_logger import logger

log = logger(__name__)
CONFIG_FILE="config.ini"

class AsyncDBConnection:
    _instance = None
    _lock = Lock()

    def __new__(cls, config_file: str = CONFIG_FILE):
        if not cls._instance:
            log.info(f"Start creating a new database client.")
            
            try:
                _config = configparser.ConfigParser()
                _config.read(config_file)
                _config.db_url = _config["database"]["MONGO_URL"]
                _config.db_name = _config["database"]["DB_NAME"]
            except Exception as e:
                raise e

            log.info(f"Database connection url : {_config.db_url}")
            log.info(f"Database connection name : {_config.db_name}")

            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)

                    try:
                        cls._instance._client = AsyncIOMotorClient(_config.db_url)
                        cls._instance._db = cls._instance._client[_config.db_name]
                    except PyMongoError as e:
                        log.error(f"Failed to connect to DB: {e}")
                        raise

                    log.info(f"A new database client is created.")
        
        return cls._instance

    def _get_client(self):
        return self._client

    def _get_db(self):
        return self._db

    def _get_collection(self, col_name):
        db = self._get_db()
        return db[col_name]
