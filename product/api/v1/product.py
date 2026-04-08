from fastapi import APIRouter

from api.service.product_service import get_product, create_product, update_product_name, update_product_stock
from api.service.product_item_service import create_product_order_item

from api.dto.product import Product, ProductOrderItem, ProductStock, Client_Data_Response, Client_Message_Response
from api.utils._message import get_api_response_messages

from api.utils.resp_codes import resp_codes
from api.models.product import ProductData, ClientProductData
from api.utils.app_logger import logger
log = logger(__name__)

router = APIRouter()

RESP_CODES=resp_codes()
_mutators = ['ADD', 'REM']
_api_responses = get_api_response_messages()

@router.post("/", tags=["product"])
def _create_product(product: Product):
    #Bloom Filters
    if product == None and product.code == None:
        log.info(f"{_api_responses['INVALID_PRODUCT_DATA']}")
        return Client_Message_Response(_api_responses['INVALID_PRODUCT_DATA'])

    response = create_product(_to_product_data(product))

    if response == None and response.message == None:
        log.info(f"{prod_code} {_api_responses['PRODUCT_NOT_CREATED']}")
        return Client_Message_Response(f"{prod_code} {_api_responses['PRODUCT_NOT_CREATED']}")

    prod_code = product.code
    response_code = response.message
    
    if response_code == RESP_CODES['OK']:
        log.info(f"{prod_code} {_api_responses['PRODUCT_CREATED']}")
        return Client_Message_Response(f"{prod_code} {_api_responses['PRODUCT_CREATED']}")
    elif response_code == RESP_CODES['DUP']:
        log.info(f"{prod_code} {_api_responses['PRODUCT_EXIST']}")
        return Client_Message_Response(f"{prod_code} {_api_responses['PRODUCT_EXIST']}")
    else:
        log.info(f"{prod_code} {_api_responses['PRODUCT_NOT_CREATED']}")
        return Client_Message_Response(f"{prod_code} {_api_responses['PRODUCT_NOT_CREATED']}")


@router.get("/{code}", tags=["product"]) #async await?
def _get_product(code: int):
    product = get_product(code)
    #print(getattr(product, "message", None))
    if product != None and product.message == RESP_CODES['OK']:
        return Client_Data_Response(_to_client_product_data(product.data))
    else:
        log.info(f"{code} {_api_responses['PRODUCT_NOT_FOUND']}")
        return Client_Message_Response(_api_responses['PRODUCT_NOT_FOUND'])

@router.put("/", tags=["product"])
def _update_product_name(product: Product):
    if product != None:
        status = update_product_name(product)
        return status
    else:
        log.info(f"{_api_responses['PRODUCT_NOT_FOUND']}")
        return _api_responses['PRODUCT_NOT_FOUND']

@router.put("/order/stock", tags=["product item"])
def _reserve_product_order_stock(productOrderItem: ProductOrderItem):
    if productOrderItem != None and productOrderItem.code >= 1000:
        response = create_product_order_item(productOrderItem)
        return response
    else:
        log.info(f"{_api_responses['PRODUCT_NOT_FOUND']}")
        return _api_responses['PRODUCT_NOT_FOUND']

@router.put("/stock", tags=["product item"])
def _update_product_stock(productStock: ProductStock):
    if productStock != None and productStock.code >= 1000 and productStock.mutator in _mutators:
        status = update_product_stock(productStock)
        return status
    else:
        log.info(f"{_api_responses['INVALID_STOCK_DATA']}")
        return _api_responses['INVALID_STOCK_DATA']



def _to_product_data(product: Product) -> ProductData:
    if not product:
        return None

    return ProductData(
        code=product.code,
        name=product.name,
        stock=_get_object_attr(product, 'stock'),
        version=_get_object_attr(product, 'version')
    )


def _to_client_product_data(data: ProductData):
    if not data:
        return None
    
    return ClientProductData(
        code=data.code,
        name=data.name,
        stock=data.stock,
        version=data.version
    )

def _get_object_attr(object, value):
    if hasattr(object, value):
        return object.value
    else:
        return None