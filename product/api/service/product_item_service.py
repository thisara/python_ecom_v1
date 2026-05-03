from api.dto.product import Service_Response, Repo_Response
from api.dto.product import ProductOrderItem, ConfirmOrderItemsRequest
from api.models.product import ProductOrderData, ProductOderItemData, OrderLineItemConfirm, OrderConfirmedData

from api.unit_of_work.product_item_uow import product_order_reservation
from api.service.product_service import get_product
from api.utils.resp_codes import resp_codes, LOW, NO_PROD_DATA, OK, NO_MATCH
from typing import Callable, List
from api.utils.app_logger import logger
from api.utils.constants import INIT_STATUS, CONF_STATUS

log = logger(__name__)
RESP_CODES=resp_codes()

def create_product_order_item(
    productOrderItem: ProductOrderItem,
    get_product_fn: Callable,
    repo_update_stock_fn: Callable,
    repo_update_product_item_fn: Callable) -> Service_Response:
#change to create product item
    product_code = productOrderItem.code
    curr_product = get_product_fn(product_code)

    if curr_product is None:
        log.warning(f"Product code not found {prod_code}!")
        return Service_Response("Product code not found!", None)

    source_product = curr_product.get_data()
    
    if source_product is None:
        log.warning(f"Product data not found for {prod_code}!")
        return Service_Response(RESP_CODES[NO_PROD_DATA], None)

    if source_product.stock >= productOrderItem.stock:
        response = product_order_reservation(
            source_product, 
            productOrderItem,
            repo_update_stock_fn,
            repo_update_product_item_fn)
        return Service_Response(response.message, None)

    return Service_Response(RESP_CODES[LOW], None)

async def get_product_order_item(
    order_number: str,
    repo_get_product_order_item_fn: Callable) -> Service_Response:

    try:
        response: Repo_Response = await repo_get_product_order_item_fn(order_number = order_number)
        response_data = response.get_all() or {}
        order_item_data = response_data.get("data")
    except Exception as e:
        log.warning(f"Error fetching order items : {e}")
        raise

    if order_item_data is not None:
        return Service_Response(message=RESP_CODES[OK], data=order_item_data)

    return Service_Response(message=None, data=None)

async def confirm_product_order_items(
    confirmOrderItemsRequest: ConfirmOrderItemsRequest,
    repo_confirm_product_order_items_fn: Callable,
    repo_get_async_product_fn: Callable) -> Service_Response:
    
    req_order_items: List[OrderLineItemConfirm] = []
    res_order_items: List[OrderLineItemConfirm] = []

    order_number: str = confirmOrderItemsRequest.orderRefernce
    order_items: List[OrderLineItem] = confirmOrderItemsRequest.productItems

    try:
        response: Service_Response = await get_product_order_item(
            order_number,
            repo_get_async_product_fn)
    except Exception as e:
        raise

    product_order_data: ProductOrderData = response.data

    if product_order_data is None:
        return Service_Response(message=None, data=None)

    prd_order_items: ProductOderItemData = product_order_data.product_items
    
    for ri in prd_order_items:
        res_order_line_confirm = _get_order_line_item(ri.code,ri.stock, ri.version, ri.status) #status from prod_items
        res_order_items.append(res_order_line_confirm)

    for oi in order_items:
        req_order_line_confirm = _get_order_line_item(oi.code, oi.stock, oi.version, INIT_STATUS)
        req_order_items.append(req_order_line_confirm)
    
    confirmed_items = [i for i in req_order_items 
                        if i.status is not CONF_STATUS 
                            and i in res_order_items 
                                and setattr(i, "status", CONF_STATUS) is None]

    #persist confirmed state!

    if len(confirmed_items) == 0:
        confirmed_order_data: OrderConfirmedData = _get_order_confirm_data(order_number, "none matched", confirmed_items)
        return Service_Response(message=RESP_CODES[NO_MATCH], data=confirmed_order_data)
    if len(confirmed_items) == len(req_order_items):
        confirmed_order_data: OrderConfirmedData = _get_order_confirm_data(order_number, "all matched", confirmed_items)
        return Service_Response(message=RESP_CODES[OK], data=confirmed_order_data)

    confirmed_order_data: OrderConfirmedData = _get_order_confirm_data(order_number, "partial matched", confirmed_items)
    return Service_Response(message=RESP_CODES[NO_MATCH], data=confirmed_order_data)


def _get_order_line_item(code:str, stock: float, version: int, status:str):
    return OrderLineItemConfirm(
        code = code,
        stock = stock,
        version = version,
        status = status)

def _get_order_confirm_data(order_number: str, status:str, confirmed_items: List[OrderLineItemConfirm]):
    return OrderConfirmedData(
        order_number = order_number,
        status = status,
        confirmed_items = confirmed_items)
