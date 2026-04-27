import asyncio
from api.utils.db_tools import get_collection, get_async_collection, get_collection_names
from api.models.order import OrderData, OrderItemData, OrderNumber
from api.utils.resp_codes import resp_codes, ERR, OK
from dataclasses import asdict
from api.utils.app_logger import logger
from pymongo.errors import DuplicateKeyError
from api.dto.order import Repo_Response
from typing import List

log = logger(__name__)
RESP_CODES=resp_codes()
COL_PRODUCT=get_collection_names().get('ORDER')
COL_ORDER_NUM=get_collection_names().get('ORDER_NUMBER')

def repo_create_order(orderData: OrderData, session = None):
    try:
        col = get_collection(COL_PRODUCT)
        data = asdict(orderData)
        if not data:
            return Repo_Response(RESP_CODES[ERR], None)

        db_response = col.insert_one(data, session=session)
        return Repo_Response(RESP_CODES[OK], {str(db_response.inserted_id)})

    except DuplicateKeyError as e:
        log.warning(f"Duplicate Order : {e}")
        raise
    except Exception as e:
        log.warning(f"Error creating order : {e}")
        raise

def repo_update_order(orderData: OrderData):
    pass

def repo_get_order(order_number: str):
    try:
        col = get_collection(COL_PRODUCT)
        data = col.find_one({"order_number":order_number})
    except Exception as e:
        raise

    if data is not None:
        return Repo_Response(message=RESP_CODES[OK], data=_to_order_data(data))

    return Repo_Response(message=None, data=None)


def repo_reserve_order_number(order_number: OrderNumber):
    try:
        col = get_collection(COL_ORDER_NUM)
        db_response = col.insert_one(asdict(order_number))
        return Repo_Response(RESP_CODES[OK], {str(db_response.inserted_id)})
    except DuplicateKeyError as e:
        log.warning(f"Duplicate Order number: {e}")
        raise
    except Exception as e:
        log.warning(f"Error creating order number: {e}")
        raise
    
    return Repo_Response(message=None, data=None)

#DT UTILS

def _to_order_data(data: dict) -> OrderData:
    if not data:
        return None

    order_items = data.get("order_items", None)
    order_item_data: List = []

    for oi in order_items:
        oid = OrderItemData(
            line_id = oi.get("line_id"),
            prod_code = oi.get("prod_code"),
            quantity = oi.get("quantity"),
            status = oi.get("status"),
            version = oi.get("version")
        )
        order_item_data.append(oid)
    
    return OrderData(
        order_number = data.get("order_number"),
        order_items = order_item_data,
        version = data.get("version"),
        status = data.get("status")
    )