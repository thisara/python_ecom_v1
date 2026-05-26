from typing import List
from api.dto.product import Service_Response
from api.utils.resp_codes import resp_codes, PAR_MATCH, OK
from api.utils.constants import ALL_MATCHED, PAR_MATCHED
from api.models.product import OrderLineItemConfirm, OrderConfirmedData

RESP_CODES=resp_codes()

def get_service_response(order_number: str, confirmed_items: List, req_order_items: List) -> Service_Response:
    if len(confirmed_items) == len(req_order_items):
        return Service_Response(message=RESP_CODES[OK], data=get_order_confirm_data(order_number, ALL_MATCHED, confirmed_items))
    else:
        return Service_Response(message=RESP_CODES[PAR_MATCH], data=get_order_confirm_data(order_number, PAR_MATCHED, confirmed_items))


def get_order_line_item(code:str, stock: float, version: int, status:str) -> OrderLineItemConfirm:
    return OrderLineItemConfirm(
        code = code,
        stock = stock,
        version = version,
        status = status)


def get_order_confirm_data(order_number: str, status:str, confirmed_items: List[OrderLineItemConfirm]) -> OrderConfirmedData:
    return OrderConfirmedData(
        order_number = order_number,
        status = status,
        confirmed_items = confirmed_items)