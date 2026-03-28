from api.dto.product import Client_Response
from api.dto.product import ProductOrderItem

from api.unit_of_work.product_item_uow import product_order_reservation
from api.service.product_service import get_product

def create_product_order_item(productOrderItem: ProductOrderItem) -> Client_Response:

    response_message = ""
    source_product = get_product(productOrderItem.code)

    if source_product != None:
        
        response_message = product_order_reservation(source_product, productOrderItem)

    return Client_Response(response_message, {})