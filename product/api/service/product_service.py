from api.models.product import ProductData, ProductDescData, ProductStockData
from api.dto.product import Product, ProductOrderItem, ProductStock, Service_Response
from api.repository.product_repository import repo_create_product, repo_update_product_desc, repo_update_product_stock, repo_get_product, repo_get_async_product
from api.utils.resp_codes import resp_codes
from datetime import datetime, timezone
from api.utils.app_logger import logger

log = logger(__name__)
RESP_CODES=resp_codes()
_mutators = ['ADD', 'REM']
__INIT_VERSION = 0
__INIT_STOCK = 0
__INIT_STATE = 'active' #move to conf, reuse in uow

def __id_serialiser(object)-> dict:
    #object["id"] = str(object["_id"])
    del object["_id"]
    return object

def create_product(productData: ProductData):
    curr_product: ProductData = None
    try:
        if productData and productData.code is not None:
            prod_code = productData.code
            curr_product = get_product(prod_code)
        print(curr_product)
        if curr_product and curr_product.data is not None:
            return Service_Response(RESP_CODES['DUP'], None)

        record_time = datetime.now(timezone.utc)

        product_data = ProductData(
            productData.code, 
            productData.name, 
            __INIT_STOCK, 
            __INIT_VERSION,
            record_time,
            record_time,
            __INIT_STATE
        )
        
        response = repo_create_product(product_data)

        if response and response.message == RESP_CODES['OK']:
            return Service_Response(RESP_CODES['OK'], None)
        
        return Service_Response(RESP_CODES['ERR'], None)

    except Exception as e:
        log.warning(f"Error creating product : {e}")
        raise RuntimeError(e)
    
def update_product_desc(productDescData: ProductDescData):
    try:
        product_code = productDescData.code
        product_name = productDescData.name

        curr_product = get_product(product_code)
        
        if curr_product is None:
            log.warning(f"Product code not found {prod_code}!")
            return Service_Response("Product code not found!", None)

        source_product = curr_product.get_data()
        
        if source_product is None:
            log.warning(f"Product data not found for {prod_code}!")
            return Service_Response("Product data not found!", None)
        
        product_version = source_product.version + 1
        updated_time = datetime.now(timezone.utc)

        product_desc_data = ProductDescData(
            product_code, 
            product_name, 
            product_version,
            updated_time
        )

        response = repo_update_product_desc(product_desc_data)

        if response and response.message == RESP_CODES['OK']:
            return Service_Response(RESP_CODES['OK'], None)

        return Service_Response(RESP_CODES['ERR'], None)
        
    except Exception as e:
        log.warning(f"Error updating product : {e}")
        raise e
    
    
def update_product_stock(productStock: ProductStock):
    try:
        prod_code = productStock.code
        new_prod_stock = float(productStock.stock)

        curr_product = get_product(prod_code)

        if curr_product is None:
            log.warning(f"Product code not found {prod_code}!")
            return Service_Response("Product code not found!", None)

        source_product = curr_product.get_data()
    
        if source_product is None:
            log.warning(f"Product data not found for {prod_code}!")
            return Service_Response("Product data not found!", None)

        source_product_version = source_product.version
        new_product_version = source_product_version + 1
        source_stock = float(source_product.stock)
        updated_time = datetime.now(timezone.utc)

        if productStock.mutator in _mutators:

            updated_stock = 0

            if productStock.mutator == 'ADD':
                updated_stock = source_stock + new_prod_stock
            elif productStock.mutator == 'REM' and source_stock >= new_prod_stock:
                updated_stock = source_stock - new_prod_stock
            else:
                return Service_Response(RESP_CODES['LOW'], None)

            product_stock_data = ProductStockData(
                prod_code, 
                updated_stock, 
                new_product_version,
                updated_time
            )

            response = repo_update_product_stock(product_stock_data)

            return Service_Response(response.message, None)

        return Service_Response(RESP_CODES['ERR'], None)
        
    except Exception as e:
        log.warning(f"Error updating product : {e}")
        raise e
    
def get_product(code: int) -> Service_Response:
    try:
        response: Repo_Response = repo_get_product(code)
        product_data = response.get_all() or {}
        resp_data = product_data.get("data")
    except Exception as e:
        log.error(f"Error in retrieving record for {code} : {e}")
        raise e

    if resp_data is not None:
        return Service_Response(message=None, data=resp_data)
    
    return Service_Response(message=None, data=None)

async def get_async_product(code: int) -> Service_Response:
    try:
        response: Repo_Response = await repo_get_async_product(code)
        product_data = response.get_all() or {}
        resp_data = product_data.get("data")
    except Exception as e:
        log.error(f"Error in retrieving record for {code} : {e}")
        raise e

    if resp_data is not None:
        return Service_Response(message=None, data=resp_data)
    
    return Service_Response(message=None, data=None)
