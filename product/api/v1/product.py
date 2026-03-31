from fastapi import APIRouter

from api.service.product_service import get_product, create_product, update_product_name, update_product_stock
from api.service.product_item_service import create_product_order_item

from api.dto.product import Product, ProductOrderItem, ProductStock
from api.utils._message import get_api_response_messages

router = APIRouter()

_mutators = ['ADD', 'REM']
_api_responses = get_api_response_messages()

@router.post("/", tags=["product"])
def _create_product(product: Product):
    #Bloom Filters
    existing_product = get_product(product.code)
    if existing_product != None:
        return _api_responses['PRODUCT_EXIST']
    else:
        message = create_product(product)
        return message

@router.get("/{code}", tags=["product"]) #async await?
def _get_product(code: int):
    product = get_product(code)
    if product != None:
        return product
    else:
        return _api_responses['PRODUCT_NOT_FOUND']

@router.put("/", tags=["product"])
def _update_product_name(product: Product):
    if product != None:
        status = update_product_name(product)
        return status
    else:
        return _api_responses['PRODUCT_NOT_FOUND']

@router.put("/order/stock", tags=["product item"])
def _reserve_product_order_stock(productOrderItem: ProductOrderItem):
    if productOrderItem != None and productOrderItem.code >= 1000:
        response = create_product_order_item(productOrderItem)
        return response
    else:
        return _api_responses['PRODUCT_NOT_FOUND']

@router.put("/stock", tags=["product item"])
def _update_product_stock(productStock: ProductStock):
    if productStock != None and productStock.code >= 1000 and productStock.mutator in _mutators:
        status = update_product_stock(productStock)
        return status
    else:
        return _api_responses['INVALID_STOCK_DATA']