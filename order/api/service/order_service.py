import uuid
from fastapi import Request
from typing import Callable
from datetime import datetime, timezone
from api.models.order import OrderData, OrderNumber, ProductOrderResponseData
from api.dto.order import OrderRequest, Repo_Response, Service_Response
from api.utils.resp_codes import NON, PAR, resp_codes, ERR, DUP, OK
from api.utils.app_logger import logger
from api.utils.constants import INIT_ORDER_NUMBER_STATUS, ALL_MATCHED, PAR_MATCHED
from api.service.utils.service_utils import map_json_to_order_response_data, to_order_data

log = logger(__name__)
RESP_CODES=resp_codes()

async def create_order(
        orderRequest: OrderRequest, 
        request: Request,
        get_order_fn: Callable,
        repo_create_order_fn: Callable,
        confirm_product_items_fn: Callable,
        repo_confirm_order_items_fn: Callable) -> Service_Response:
    
    if orderRequest is None:
        return Service_Response(RESP_CODES[ERR], None)

    current_order: OrderData = None

    try:
        if orderRequest and orderRequest.order_number is not None:
            order_number = orderRequest.order_number            
            current_order = await get_order_fn(order_number)

        if current_order and current_order.data is not None:
            return Service_Response(message=RESP_CODES[DUP], data=None)

        order_data: OrderData = to_order_data(orderRequest)

        """ TODO: repo_create_order_fn, confirm_product_items_fn and 
        repo_confirm_order_items_fn should be a sync transaction or part of async workflow. """

        create_response = await repo_create_order_fn(order_data)
        
        if create_response and create_response.message == RESP_CODES[OK]:

            confirm_response = await confirm_product_items_fn(order_data, request)
            
            conf_order_data: ProductOrderResponseData = map_json_to_order_response_data(confirm_response)

            if len(conf_order_data.confirmed_items) == 0:
                return Service_Response(RESP_CODES[NON], None)

            order_itm_confirm_response: Repo_Response = await repo_confirm_order_items_fn(conf_order_data)

            if order_itm_confirm_response.message == RESP_CODES[OK]:
                if conf_order_data.status == ALL_MATCHED:
                    return Service_Response(RESP_CODES[OK], None)
                if conf_order_data.status == PAR_MATCHED:
                    return Service_Response(RESP_CODES[PAR], None)
            
        return Service_Response(RESP_CODES[ERR], None)

    except Exception as e:
        log.warning(f"Error creating order : {e}")
        raise


async def get_order(
        order_number: str,
        get_order_repo_fn: Callable) -> Service_Response:

    try:
        response = await get_order_repo_fn(order_number)
        order_data = response.get_all() or {}
        resp_data = order_data.get("data")
    except Exception as e:
        raise

    if resp_data is not None:
        return Service_Response(message=RESP_CODES[OK], data=resp_data)

    return Service_Response(message=None, data=None)


async def reserve_order_number(
        reserve_order_number_repo_fn=Callable) -> Service_Response:

    record_time = datetime.now(timezone.utc)

    try:
        order_number = OrderNumber(
            order_number = uuid.uuid1(),
            version = 1,
            status = INIT_ORDER_NUMBER_STATUS,
            date_created = record_time,
            date_updated = record_time,
            is_active = True)
        response = await reserve_order_number_repo_fn(order_number)
    except Exception as e:
        raise

    if response and response.message == RESP_CODES[OK]:
        return Service_Response(message=RESP_CODES[OK], data=order_number)
    
    return Service_Response(message=None, data=None)

