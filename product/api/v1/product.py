from fastapi import APIRouter, Depends, HTTPException

from api.service.product_service import get_async_product, create_product, update_product_desc, update_product_stock
from api.service.product_item_service import create_product_order_item

from api.dto.product import Product, ProductOrderItem, ProductStock, Client_Data_Response, Client_Message_Response
from api.models.product import ProductData, ProductDescData, ClientProductData

from api.utils.message import get_api_response_messages, get_mutators
from api.utils.resp_codes import resp_codes
from .utils.data_mapper import to_product_data, to_product_desc_data, to_client_product_data
from api.utils.app_logger import logger

from api.service.product_service_dep import get_product_dep, update_product_dep, create_product_dep, update_product_stock_dep, get_product_async_dep
from api.service.product_item_service_dep import update_product_item_stock_dep

log = logger(__name__)
router = APIRouter()

RESP_CODES=resp_codes()
mutators = get_mutators()
api_responses = get_api_response_messages()

@router.post("/", tags=["product"])
def create_product_endpoint(
    product: Product,
    get_product_fn=Depends(get_product_dep),
    repo_create_fn=Depends(create_product_dep)):

    if product is None:
        log.warning(f"Invalid product data provided.")
        return Client_Message_Response(api_responses['INVALID_PRODUCT_DATA'])

    try:
        prod_code = product.code
        response = create_product(
            to_product_data(product),
            get_product_fn=get_product_fn,
            repo_create_fn=repo_create_fn)

    except Exception as e:
        log.warning(f"Error creating product : {e}")
        raise HTTPException(status_code=500, detail=f"Error creating Product code {prod_code} : {e}")
    
    response_code = getattr(response, "message", None)

    if response_code is not None and response_code == RESP_CODES['OK']:
        log.info(f"{prod_code} {api_responses['PRODUCT_CREATED']}")
        return Client_Message_Response(f"{prod_code} {api_responses['PRODUCT_CREATED']}")
    
    if response_code is not None and response_code == RESP_CODES['DUP']:
        log.info(f"{prod_code} {api_responses['PRODUCT_EXIST']}")
        raise HTTPException(status_code=409, detail=f"{prod_code} {api_responses['PRODUCT_EXIST']}")
    
    log.warning(f"{prod_code} {api_responses['PRODUCT_NOT_CREATED']}")
    raise HTTPException(status_code=400, detail=f"Something wrong creating {prod_code}.")


@router.get("/{code}", tags=["product"])
async def get_product_endpoint(
    code: int,
    get_product_async_fn=Depends(get_product_async_dep)):

    try:
        response = await get_product_async_fn(code)
    except Exception as e:
        log.warning(f"Error fetching Product Code {code} : {e}")
        raise HTTPException(status_code=500, detail=api_responses['INTERNAL_ERROR']) 

    data = getattr(response, "data", None)

    if data is not None:
        return Client_Data_Response(to_client_product_data(data))

    log.warning(f"Product {code} not found!")
    raise HTTPException(status_code=404, detail=api_responses['PRODUCT_NOT_FOUND'])


@router.put("/", tags=["product"])
def update_product_desc_endpoint(
    product: Product,
    get_product_fn=Depends(get_product_dep),
    repo_update_fn=Depends(update_product_dep)):

    if product is None:
        raise HTTPException(status_code=400, detail=f"{api_responses['PRODUCT_NOT_UPDATED']}")

    prod_code = product.code

    try:
        response = update_product_desc(
            to_product_desc_data(product),
            get_product_fn=get_product_fn,
            repo_update_fn=repo_update_fn)

    except Exception as e:
        log.warning(f"Error updating product : {e}")
        raise HTTPException(status_code=500, detail=f"Error updating product code {prod_code}!")

    response_code = getattr(response, "message", None)

    if response_code is not None and response_code == RESP_CODES['OK']:
        log.info(f"Product code : {prod_code} is updated!")
        return Client_Message_Response(f"{prod_code} {api_responses['PRODUCT_UPDATED']}")
    
    log.warning(f"Product code : {product} is not updated!")
    raise HTTPException(status_code=400, detail=f"{api_responses['PRODUCT_NOT_UPDATED']}")


@router.put("/order/stock", tags=["product stock"])
def reserve_product_order_stock_endpoint(
    productOrderItem: ProductOrderItem,
    get_product_fn=Depends(get_product_dep),
    repo_update_stock_fn=Depends(update_product_stock_dep),
    repo_update_product_item_fn=Depends(update_product_item_stock_dep)):
    if productOrderItem is not None:
        try:
            response = create_product_order_item(
                productOrderItem,
                get_product_fn=get_product_fn,
                repo_update_stock_fn=repo_update_stock_fn,
                repo_update_product_item_fn=repo_update_product_item_fn)
        except Exception as e:
            log.warning(f"Error reserving product items.")
            raise HTTPException(status_code=500, detail=f"Error reserving products.")

    response_code = getattr(response, "message", None)

    if response_code is not None and response_code == RESP_CODES['OK']:
        log.info(f"Product reserved successfully for product code : {productOrderItem.code}")
        return Client_Message_Response(f"{productOrderItem.code} {api_responses['PRODUCT_RESERVED']}")

    if response_code is not None and response_code == RESP_CODES['LOW']:
        log.info(f"Low product stock available for product code : {productOrderItem.code}")
        return Client_Message_Response(f"{productOrderItem.code} {api_responses['PRODUCT_LOW_STOCK']}")

    if response_code is not None and response_code == RESP_CODES['VER']:
        log.warning(f"Update requested on stale version of product code : {productOrderItem.code}")
        return Client_Message_Response(f"{productOrderItem.code} {api_responses['PRODUCT_VER_INCORRECT']}")

    log.warning(f"{api_responses['PRODUCT_NOT_RESERVED']}")
    return HTTPException(status_code=400, detail=f"{api_responses['PRODUCT_NOT_RESERVED']}")
        

@router.put("/stock", tags=["product stock"])
def update_product_stock_endpoint(
    productStock: ProductStock,
    get_product_fn=Depends(get_product_dep),
    repo_update_stock_fn=Depends(update_product_stock_dep)):

    if productStock is None or productStock.mutator not in mutators:
        raise HTTPException(status_code=400, detail=f"{api_responses['PRODUCT_NOT_UPDATED']}")
        
    prod_code = productStock.code

    try:
        response = update_product_stock(
            productStock,
            get_product_fn=get_product_fn,
            repo_update_stock_fn=repo_update_stock_fn)

    except Exception as e:
        log.warning(f"Error updating product : {e}")
        raise HTTPException(status_code=500, detail=f"Error updating product code {prod_code}!")

    response_code = getattr(response, "message", None)

    if response is not None and response_code == RESP_CODES['OK']:
        log.info(f"Product code : {prod_code} is updated!")
        return Client_Message_Response(f"{prod_code} {api_responses['PRODUCT_UPDATED']}")
    
    if response is not None and response_code == RESP_CODES['LOW']:
        log.info(f"Product code : {prod_code} has low stock!")
        return Client_Message_Response(f"{prod_code} {api_responses['PRODUCT_LOW_STOCK']}")

    log.warning(f"Product : {productStock} is not updated!")
    raise HTTPException(status_code=400, detail=f"{api_responses['PRODUCT_NOT_UPDATED']}")
