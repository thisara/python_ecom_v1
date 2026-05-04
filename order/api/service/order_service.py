from api.models.order import OrderData, OrderItemData, OrderNumber, OrderLineItemConfirm, OrderItemConfirm
from api.dto.order import OrderRequest, Service_Response
from api.repository.order_repository import repo_create_order, repo_get_order, repo_reserve_order_number
from api.utils.resp_codes import resp_codes, ERR, DUP, OK
import uuid
import requests
from typing import List
from datetime import datetime, timezone
from api.utils.app_logger import logger
import json
from dataclasses import asdict

log = logger(__name__)
RESP_CODES=resp_codes()

def create_order(orderRequest: OrderRequest):
    if orderRequest is None:
        return Service_Response(RESP_CODES[ERR], None)

    current_order: OrderData = None
    try:
        if orderRequest and orderRequest.order_number is not None:
            order_number = orderRequest.order_number            
            current_order = get_order(order_number)

        if current_order and current_order.data is not None:
            return Service_Response(message=RESP_CODES[DUP], data=None)

        order_data: OrderData = _to_order_data(orderRequest)

        #TX:
        response = repo_create_order(order_data)
        
        if response and response.message == RESP_CODES[OK]:
            #ASYNC : confirm product item consumption - send to Kafka
            confirm_product_items(order_data)
            return Service_Response(RESP_CODES[OK], None)

        return Service_Response(RESP_CODES[ERR], None)

    except Exception as e:
        log.warning(f"Error creating order : {e}")
        raise

def get_order(order_number: str) -> Service_Response:
    try:
        response = repo_get_order(order_number)
        order_data = response.get_all() or {}
        resp_data = order_data.get("data")
    except Exception as e:
        raise

    if resp_data is not None:
        return Service_Response(message=RESP_CODES[OK], data=resp_data)

    return Service_Response(message=None, data=None)


def reserve_order_number():

    record_time = datetime.now(timezone.utc)

    try:
        order_number = OrderNumber(
            order_number = uuid.uuid1(),
            version = 1,
            status = 'active',
            date_created = record_time,
            date_updated = record_time,
            is_active = True)
        response = repo_reserve_order_number(order_number)
    except Exception as e:
        raise

    if response and response.message == RESP_CODES[OK]:
        return Service_Response(message=RESP_CODES[OK], data=order_number)
    
    return Service_Response(message=None, data=None)


#--

def _to_order_data(orderRequest: OrderRequest) -> OrderData:

    record_time = datetime.now(timezone.utc).isoformat()

    if not orderRequest:
        return None

    if not orderRequest.order_items:
        return None

    order_line_items: List = []

    for i in orderRequest.order_items:
        item_data = OrderItemData(
            line_id = i.line_id,
            prod_code = i.product_code,
            quantity = i.quantity,
            status = 'recieved',
            version = i.version,
            date_created = record_time,
            date_updated = record_time,
            is_active = True)

        order_line_items.append(item_data)

    return OrderData(
        order_number = orderRequest.order_number,
        order_items = order_line_items,
        version = 0,
        status = 'recieved',
        date_created = record_time, 
        date_updated = record_time,
        is_active = True)


def confirm_product_items(orderData: OrderData):
    api_call(orderData)

def api_call(order_data: OrderData):

    order_number: str = order_data.order_number
    line_items: List[OrderItemData] = order_data.order_items

    c_lines: List = []

    for i in line_items:
        line = OrderLineItemConfirm(
            code = i.prod_code,
            stock = i.quantity,
            version = i.version)
        c_lines.append(line)

    order: OrderItemConfirm = OrderItemConfirm(
        orderRefernce = order_number,
        productItems = c_lines
    )

    rest_order = json.dumps(asdict(order))
    print(f"-------->> : {rest_order}")

    url: str = "http://127.0.0.1:8001/product/order/items"
    response = requests.put(url, rest_order)

    print(f"response : {response.json()}")

    #Handdle matched, partial-matched, non-matched, error
    