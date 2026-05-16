from api.dto.product import Service_Response
from product.tests.product import RESP_CODES

def fake_update_product_item():
    return Service_Response(RESP_CODES['OK'], None) 