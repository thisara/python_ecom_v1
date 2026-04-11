from api.dto.product import Service_Response, Repo_Response
from api.dto.product import ProductOrderItem

from api.unit_of_work.product_item_uow import product_order_reservation
from api.service.product_service import get_product
from api.utils.resp_codes import resp_codes

RESP_CODES=resp_codes()

def create_product_order_item(productOrderItem: ProductOrderItem) -> Service_Response:

    product_code = productOrderItem.code
    curr_product = get_product(product_code)
        
    if curr_product is None:
        log.warning(f"Product code not found {prod_code}!")
        return Service_Response("Product code not found!", None)

    source_product = curr_product.get_data()
    
    if source_product is None:
        log.warning(f"Product data not found for {prod_code}!")
        return Service_Response("Product data not found!", None)

    if source_product.stock >= productOrderItem.stock:
        response = product_order_reservation(source_product, productOrderItem)
        return Service_Response(response.message, None)

    return Service_Response(RESP_CODES['LOW'], None)