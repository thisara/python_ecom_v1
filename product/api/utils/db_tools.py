from ._db_client import DBConnection
from ._db_async_client import AsyncDBConnection

def get_db():
    db = DBConnection()
    return db._get_db()

def get_client():
    db = DBConnection()
    return db._get_client()

def get_collection(col_name):
    db = DBConnection()
    return db._get_collection(col_name)

def get_collection_names() -> str:
    collections: dict = {
        "PRODUCT": "product",
        "PRODUCT_ITEM": "product_order_item"
    }
    return collections

def get_async_db():
    db = AsyncDBConnection()
    return db._get_db()

def get_async_client():
    db = AsyncDBConnection()
    return db._get_client()

def get_async_collection(col_name):
    db = AsyncDBConnection()
    return db._get_collection(col_name)
    