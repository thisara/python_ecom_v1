from api.utils._db_client import DBConnection 
from api.models.product import ProductData
#from pymongo.collection import Collection
#from pymongo import MongoClient
from api.dto.product import Repo_Response

from pymongo.errors import DuplicateKeyError

#client = get_mongo_client()
#db = get_db_conn(client)
COL_PRODUCT="product"

def repo_update_product(productData:ProductData, client = None, session = None):
    result: Repo_Response = Repo_Response(None, None)
    try:
        db_connection = DBConnection(client)
        col = db_connection.get_collection(COL_PRODUCT)
        #col = _get_db_conn(COL_PRODUCT, client)
        #col = db[COL_PRODUCT]
        db_response = col.update_one(
            { "code": productData.code},
            { "$set":{"stock": productData.stock, "version": productData.version}},
            session=session
        )
        result = Repo_Response("Added successfully", {str(db_response.inserted_id)})
    except Exception as e:
        raise e

    return result

#optional client / session
def repo_create_product(productData: ProductData, client = None, session = None):
    result: Repo_Response = Repo_Response(None, None)
    try:
        db_connection = DBConnection(client)
        col = db_connection.get_collection(COL_PRODUCT)
        data = productData.__dict__.copy()
        print(data)
        if not data:
            result = Repo_Response("Error in Product data", {})
        else:
            db_response = col.insert_one(data)
            result = Repo_Response("Added successfully", {str(db_response.inserted_id)})
    
    except DuplicateKeyError as e:
        raise e
    except Exception as e:
        raise e

    return result

def repo_update_product_name(productData: ProductData, client = None, session = None):
    result: Repo_Response = Repo_Response(None, None)
    try:
        db_connection = DBConnection(client)
        col = db_connection.get_collection(COL_PRODUCT)
        #data = product_data.__dict__.copy()
        col.update_one(
                { "code": productData.code},
                { "$set":{"name": productData.name, "version": productData.version}},
            upsert=False)

    except Exception as e:
        raise e
    
    return result

def repo_update_product_stock(productData: ProductData, client = None, session = None):
    result: Repo_Response = Repo_Response(None, None)
    try:
        db_connection = DBConnection(client)
        col = db_connection.get_collection(COL_PRODUCT)

        col.update_one(
                { "code": productData.code},
                { "$set":{"stock": productData.stock, "version": productData.version}},
            upsert=False)

    except Exception as e:
        raise e
    
    return result

def repo_get_product(code: int):
    result: Repo_Response = Repo_Response(None, None)
    try:
        db_connection = DBConnection()
        col = db_connection.get_collection(COL_PRODUCT)
        product = col.find_one({"code": code})

        result = Repo_Response("FOUND", product)
    except Exception as e:
        raise e

    return result
    