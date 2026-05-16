from datetime import datetime, timezone
from typing import List
from api.models.order import OrderData, OrderItemData, OrderItemData, ProductOrderItemResponseData, ProductOrderResponseData
from api.dto.order import OrderRequest
from api.utils.constants import INIT_ORDER_ITEM_STATUS, INIT_ORDER_VERSION, INIT_ORDER_STATUS

def to_order_data(orderRequest: OrderRequest) -> OrderData:

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
            status = INIT_ORDER_ITEM_STATUS,
            version = i.version,
            date_created = record_time,
            date_updated = record_time,
            is_active = True)

        order_line_items.append(item_data)

    return OrderData(
        order_number = orderRequest.order_number,
        order_items = order_line_items,
        version = INIT_ORDER_VERSION,
        status = INIT_ORDER_STATUS,
        date_created = record_time, 
        date_updated = record_time,
        is_active = True)


def map_json_to_order_response_data(json_data: dict) -> ProductOrderResponseData:
    
    data = json_data.get("data", {})
    
    order_number = data.get("order_number")
    confirmed_status = data.get("status")
    confirmed_items = data.get("confirmed_items", [])

    line_items = []
    for item in confirmed_items:

        line_item = ProductOrderItemResponseData(
            prod_code=item.get("code"),
            quantity=item.get("stock"),
            version=item.get("version"),
            status=item.get("status")
        )
        line_items.append(line_item)

    return ProductOrderResponseData(
        order_number=order_number,
        confirmed_items=line_items,
        status=confirmed_status
    )

