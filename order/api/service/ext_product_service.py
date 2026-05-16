import os
import json
from dataclasses import asdict
from typing import List
from fastapi import Request
from api.models.order import OrderData, OrderItemConfirm, OrderItemData, OrderLineItemConfirm
from api.service.api_client import api_client
from api.utils.config import get_api_endpoints

api_endpoints=get_api_endpoints()

async def confirm_product_items(order_data: OrderData, request: Request):

    order_number: str = order_data.order_number
    line_items: List[OrderItemData] = order_data.order_items

    order_lines: List = []

    for i in line_items:
        line = OrderLineItemConfirm(
            code = i.prod_code,
            stock = i.quantity,
            version = i.version)
        order_lines.append(line)

    order: OrderItemConfirm = OrderItemConfirm(
        orderRefernce = order_number,
        productItems = order_lines)

    rest_order: dict = json.dumps(asdict(order))
    endpoint: str = f"{os.getenv('PRODUCT_API_BASE_URL')}{api_endpoints['PRODUCT_ORDER_ITEM']}"

    return await api_client(
        request=request,
        method="PUT",
        url=endpoint,
        data=rest_order)

