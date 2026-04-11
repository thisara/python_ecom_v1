from api.utils._db_client import get_collection
from api.models.product import ProductData, ProductDescData, ProductStockData
from api.dto.product import Repo_Response
from pymongo.errors import DuplicateKeyError
from api.utils.resp_codes import resp_codes
from api.utils.app_logger import logger

log = logger(__name__)
RESP_CODES=resp_codes()
COL_PRODUCT="product"

def repo_update_product(productData:ProductData, client = None, session = None):
    try:
        col = get_collection(COL_PRODUCT)
        db_response = col.update_one(
            { "code": productData.code},
            { "$set":{"stock": productData.stock, "version": productData.version}},
            session=session
        )
        return Repo_Response(RESP_CODES['OK'], None)

    except Exception as e:
        raise e


#optional client / session
def repo_create_product(productData: ProductData, client = None, session = None):
    try:
        col = get_collection(COL_PRODUCT)
        data = productData.__dict__.copy()
        if not data:
            return Repo_Response(RESP_CODES['ERR'], None)
        
        db_response = col.insert_one(data)
        return Repo_Response(RESP_CODES['OK'], {str(db_response.inserted_id)})
    
    except DuplicateKeyError as e:
        raise e
    except Exception as e:
        raise e


def repo_update_product_desc(productDescData: ProductDescData, client = None, session = None):
    try:
        col = get_collection(COL_PRODUCT)
        data = productDescData.__dict__.copy()
        if not data:
            return Repo_Response(RESP_CODES['ERR'], None)

        db_response = col.update_one(
                { "code": data.get("code")},
                { "$set":{"name": data.get("name"), "version": data.get("version")}},
            upsert=False)

        return Repo_Response(RESP_CODES['OK'], None)

    except Exception as e:
        raise e


def repo_update_product_stock(productStockData: ProductStockData, client = None, session = None):
    try:
        col = get_collection(COL_PRODUCT)
        db_response = col.update_one(
                { "code": productStockData.code},
                { "$set":{"stock": productStockData.stock, "version": productStockData.version}},
            upsert=False)
        return Repo_Response(RESP_CODES['OK'], None)
        
    except Exception as e:
        raise e


def repo_get_product(code: int) -> Repo_Response:
    try:
        col = get_collection(COL_PRODUCT)
        data = col.find_one({"code": code})
    except Exception as e:
        log.info(f"Error in fetching {code} : {e}")
        raise
    
    if data is not None:
        return Repo_Response(message=None, data=_to_product(data))
        
    return Repo_Response(message=None, data=None)
    
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
    