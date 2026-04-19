from api.models.product import ProductData
from api.dto.product import Service_Response
from api.utils.resp_codes import resp_codes

RESP_CODES=resp_codes()

def fake_get_product(code):
    prodData = ProductData(code=str(1001),
                name='Test Product 1',
                stock=38.0,
                version=93)
    return Service_Response(message=RESP_CODES['OK'], data=prodData)

async def fake_async_get_product(code):
    prodData = ProductData(code=str(1001),
                name='Test Product 1',
                stock=38.0,
                version=93)
    return Service_Response(message=RESP_CODES['OK'], data=prodData)

def fake_get_empty_product(code):
    return Service_Response(message=None, data=None)

def fake_update_product_desc(data):
    return Service_Response(RESP_CODES['OK'], None)

def fake_update_empty_product_desc(data):
    return Service_Response(RESP_CODES['NO_PROD'], None)

def fake_update_product_stock(data):
    return Service_Response(RESP_CODES['OK'], None)

def fake_update_empty_product_stock(data):
    return Service_Response(RESP_CODES['OK'], None)

def fake_create_product(data):
    return Service_Response(RESP_CODES['OK'], None)