from api.utils.db_tools import get_collection, get_collection_names, get_async_collection
from api.models.product import ProductOderItemData, ProductOrderData, OrderConfirmedData, OrderLineItemConfirm
from api.dto.product import Repo_Response
from dataclasses import asdict
from api.utils.resp_codes import resp_codes, OK, ERR
from api.utils.app_logger import logger

from pymongo import UpdateOne

log = logger(__name__)
RESP_CODES=resp_codes()
COL_PRODUCT_ITEM=get_collection_names().get('PRODUCT_ITEM')

def repo_create_product_item(prodcutOrderItemData:ProductOderItemData, session = None) -> Repo_Response:
    try:
        col = get_collection(COL_PRODUCT_ITEM)
        data = asdict(prodcutOrderItemData)

        if not data:
            log.warning("Error in data!")
            return Repo_Response(RESP_CODES[ERR], {})
 
        db_response = col.insert_one(data, session=session)
        log.info("Added successfully!")
        return Repo_Response(RESP_CODES[OK], {str(db_response.inserted_id)})
    
    except Exception as e:
        log.warning("Error creating product item!")
        raise


async def repo_get_product_order_item(order_number: str, session = None) -> Repo_Response:
    try:
        col = get_async_collection(COL_PRODUCT_ITEM)
        data = await col.find({"orderRef": order_number}).to_list(length=100)
        return Repo_Response(RESP_CODES[OK], data=_to_product_items(order_number, data))

    except Exception as e:
        log.warning(f"Error fetching product items for order : {order_number}")
        raise


async def repo_confirm_product_order_items(order_confirm:OrderConfirmedData, session = None) -> Repo_Response:
    
    order_number: str = order_confirm.order_number
    order_line_items: List[OrderLineItemConfirm] = order_confirm.confirmed_items
    order_status: str = order_confirm.status

    updates = []
    for ri in order_line_items:
        v = UpdateOne({"orderRef": order_number, "code": ri.code}, {"$set": {"status": order_status}})
        updates.append(v)
    try:
        col = get_async_collection(COL_PRODUCT_ITEM)
        res = col.bulk_write(updates, session=session)
    except Exception as e:
        log.warning(f"Error confirming order items!")
        raise
    return Repo_Response(RESP_CODES[OK], data=None)


#---

def _to_product_items(order_number: str, data: dict) -> ProductOrderData:
    if not data:
        return None
    
    items: ProductOderItemData = []

    for d in data:
        items.append(ProductOderItemData(
            order_item_id=d.get("order_item_id"),
            code=d.get("code"),
            orderRef=d.get("orderRef"),
            stock=d.get("stock"),
            version=d.get("version"),
            status=d.get("status"),
            date_created=d.get("date_created"),
            date_updated=d.get("date_updated"),
            is_active=d.get("is_active")))
    
    return ProductOrderData(
        order_number=order_number,
        product_items=items)