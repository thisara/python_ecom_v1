from api.utils.db_tools import get_collection, get_async_collection, get_collection_names
from api.models.product import ProductData, ProductDescData, ProductStockData
from api.dto.product import Repo_Response
from pymongo.errors import DuplicateKeyError
from api.utils.resp_codes import resp_codes
from dataclasses import asdict
import asyncio
from api.utils.app_logger import logger

log = logger(__name__)
RESP_CODES=resp_codes()
COL_PRODUCT=get_collection_names().get('PRODUCT')

#??remove?
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
        raise


#optional client / session
def repo_create_product(productData: ProductData, client = None, session = None):
    try:
        col = get_collection(COL_PRODUCT)
        data = asdict(productData)
        if not data:
            return Repo_Response(RESP_CODES['ERR'], None)
        
        db_response = col.insert_one(data)
        return Repo_Response(RESP_CODES['OK'], {str(db_response.inserted_id)})
    
    except DuplicateKeyError as e:
        raise
    except Exception as e:
        raise


def repo_update_product_desc(productDescData: ProductDescData, client = None, session = None):
    try:
        col = get_collection(COL_PRODUCT)
        data = asdict(productDescData)
        if not data:
            return Repo_Response(RESP_CODES['ERR'], None)

        db_response = col.update_one(
                { "code": data.get("code")},
                { "$set":{
                    "name": data.get("name"), 
                    "version": data.get("version"),
                    "date_updated": data.get("date_updated")}},
            upsert=False)

        return Repo_Response(RESP_CODES['OK'], None)

    except Exception as e:
        raise


def repo_update_product_stock(productStockData: ProductStockData, client = None, session = None):
    try:
        col = get_collection(COL_PRODUCT)
        data = asdict(productStockData)
        db_response = col.update_one(
                { "code": productStockData.code},
                { "$set":{
                    "stock": data.get("stock"), 
                    "version": data.get("version"),
                    "date_updated": data.get("date_updated")}},
            upsert=False)
        return Repo_Response(RESP_CODES['OK'], None)
        
    except Exception as e:
        raise

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

async def repo_get_async_product(code: int) -> Repo_Response:
    try:
        col = get_async_collection(COL_PRODUCT)
        data = await col.find_one({"code": code})
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
    