from typing import List
from datetime import datetime
from api.models.order import OrderData, OrderItemData

TIMESTAMP_FORMAT="%Y-%m-%d %H:%M:%S %Z"

def to_order_data(data: dict) -> OrderData:
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
            version = oi.get("version"),
            date_created = _to_local_timestamp(
                data.get("date_created"), TIMESTAMP_FORMAT),
            date_updated = _to_local_timestamp(
                data.get("date_updated"), TIMESTAMP_FORMAT),
            is_active = data.get("is_active")
        )
        order_item_data.append(oid)
    
    return OrderData(
        order_number = data.get("order_number"),
        order_items = order_item_data,
        version = data.get("version"),
        status = data.get("status"),
        date_created = _to_local_timestamp(
            data.get("date_created"), TIMESTAMP_FORMAT),
        date_updated = _to_local_timestamp(
            data.get("date_updated"), TIMESTAMP_FORMAT),
        is_active = data.get("is_active")
    )


def _to_local_timestamp(timestamp:str, time_format:str) -> str:
    return datetime.fromisoformat(timestamp).astimezone().strftime(
                                time_format)