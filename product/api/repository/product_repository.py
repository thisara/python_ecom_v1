from api.utils._db_client import DBConnection 
from api.models.product import ProductData
from api.dto.product import Repo_Response
from pymongo.errors import DuplicateKeyError
from api.utils.resp_codes import resp_codes
from api.utils.app_logger import logger

log = logger(__name__)
RESP_CODES=resp_codes()
COL_PRODUCT="product"

def repo_update_product(productData:ProductData, client = None, session = None):
    result: Repo_Response = Repo_Response(None, None)
    try:
        db_connection = DBConnection(client)
        col = db_connection.get_collection(COL_PRODUCT)
        db_response = col.update_one(
            { "code": productData.code},
            { "$set":{"stock": productData.stock, "version": productData.version}},
            session=session
        )
        result = Repo_Response(RESP_CODES['OK'], None)

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

        if not data:
            result = Repo_Response(RESP_CODES['ERR'], None)
        else:
            db_response = col.insert_one(data)
            result = Repo_Response(RESP_CODES['OK'], {str(db_response.inserted_id)})
    
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

        db_response = col.update_one(
                { "code": productData.code},
                { "$set":{"name": productData.name, "version": productData.version}},
            upsert=False)

        result = Repo_Response(RESP_CODES['OK'], None)

    except Exception as e:
        raise e
    
    return result

def repo_update_product_stock(productData: ProductData, client = None, session = None):
    result: Repo_Response = Repo_Response(None, None)
    try:
        db_connection = DBConnection(client)
        col = db_connection.get_collection(COL_PRODUCT)

        db_response = col.update_one(
                { "code": productData.code},
                { "$set":{"stock": productData.stock, "version": productData.version}},
            upsert=False)
        result = Repo_Response(RESP_CODES['OK'], None)
        
    except Exception as e:
        raise e
    
    return result

def repo_get_product(code: int) -> Repo_Response:
    result: Repo_Response = Repo_Response(None, None)
    try:
        db_connection = DBConnection()
        col = db_connection.get_collection(COL_PRODUCT)
        data = col.find_one({"code": code})
        if data != None:
            result = Repo_Response(RESP_CODES['OK'], _to_product(data))
        else:
            result = Repo_Response(RESP_CODES['ERR'], None)
    except Exception as e:
        log.info(f"Error in fetching {code} - {e}")
        raise e

    return result

#DT UTILS

def _to_product(data: dict) -> ProductData:
    if not data:
        return None

    return ProductData(
        code=data.get("code"),
        name=data.get("name"),
        stock=data.get("stock"),
        version=data.get("version")
    )
    