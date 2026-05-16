from dataclasses import asdict
from pymongo import UpdateOne
from pymongo.results import BulkWriteResult
from pymongo.errors import DuplicateKeyError
from api.utils.db_tools import get_async_collection, get_collection_names
from api.utils.resp_codes import resp_codes, ERR, OK
from api.utils.app_logger import logger
from api.models.order import OrderData, OrderNumber, ProductOrderResponseData
from api.dto.order import Repo_Response
from api.repository.utils.repository_utils import to_order_data

log = logger(__name__)
RESP_CODES=resp_codes()
COL_PRODUCT=get_collection_names().get('ORDER')
COL_ORDER_NUM=get_collection_names().get('ORDER_NUMBER')

async def repo_create_order(orderData: OrderData, session = None):
    try:
        col = get_async_collection(COL_PRODUCT)
        data = asdict(orderData)
        if not data:
            return Repo_Response(RESP_CODES[ERR], None)

        db_response = await col.insert_one(data, session=session)
        return Repo_Response(RESP_CODES[OK], {str(db_response.inserted_id)})

    except DuplicateKeyError as e:
        log.warning(f"Duplicate Order : {e}")
        raise
    except Exception as e:
        log.warning(f"Error creating order : {e}")
        raise

async def repo_confirm_order_items(prodResponseData: ProductOrderResponseData):
    try:
        col = get_async_collection(COL_PRODUCT)
        order_number = prodResponseData.order_number
        confirmed_items = prodResponseData.confirmed_items

        print(order_number)
        print(confirmed_items)

        updates = []
        for ci in confirmed_items:
            item = UpdateOne(
                {"order_number": order_number, "order_items.prod_code": ci.prod_code},
                 {"$set": {"order_items.$.status": ci.status}})
            updates.append(item)

        result: BulkWriteResult = await col.bulk_write(updates)

        if result.modified_count == len(confirmed_items):
            return Repo_Response(RESP_CODES[OK], None)
        
        return Repo_Response(RESP_CODES[ERR], None)
    
    except Exception as e:
        raise

async def repo_get_order(order_number: str):
    try:
        col = get_async_collection(COL_PRODUCT)
        data = await col.find_one({"order_number":order_number})
    except Exception as e:
        raise

    if data is not None:
        return Repo_Response(message=RESP_CODES[OK], data=to_order_data(data))

    return Repo_Response(message=None, data=None)


async def repo_reserve_order_number(order_number: OrderNumber):
    try:
        col = get_async_collection(COL_ORDER_NUM)
        db_response = await col.insert_one(asdict(order_number))
        return Repo_Response(RESP_CODES[OK], {str(db_response.inserted_id)})
    except DuplicateKeyError as e:
        log.warning(f"Duplicate Order number: {e}")
        raise
    except Exception as e:
        log.warning(f"Error creating order number: {e}")
        raise

