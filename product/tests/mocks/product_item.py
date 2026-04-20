from api.dto.product import Service_Response

def fake_update_product_item():
    return Service_Response(RESP_CODES['OK'], None) 