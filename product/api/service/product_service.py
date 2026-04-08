from api.models.product import ProductData
from api.dto.product import Product, ProductOrderItem, ProductStock, Service_Response
from api.repository.product_repository import repo_create_product, repo_update_product_name, repo_update_product_stock, repo_get_product
from api.utils.resp_codes import resp_codes
from api.utils.app_logger import logger

log = logger(__name__)
RESP_CODES=resp_codes()
__INIT_VERSION = 0
__INIT_STOCK = 0

def __id_serialiser(object)-> dict:
    #object["id"] = str(object["_id"])
    del object["_id"]
    return object

def create_product(productData: ProductData):
    curr_product: ProductData = None
    try:
        if productData != None and productData.code != None:
            prod_code = productData.code
            curr_product = get_product(prod_code)

        if curr_product != None and curr_product.data != None:
            return Service_Response(RESP_CODES['DUP'], None)

        product_data = ProductData(productData.code, productData.name, __INIT_STOCK, __INIT_VERSION)
        
        response = repo_create_product(product_data)

        if response != None and response.message == RESP_CODES['OK']:
            return Service_Response(RESP_CODES['OK'], None)
        else:
            return Service_Response(RESP_CODES['ERR'], None)
    except Exception as e:
        log.info(f"Error creating product : {e}")
        return Service_Response(RESP_CODES['ERR'], None)
    
def update_product_name(product: Product):
    response_message = ""
    try:
        product_code = product.code
        product_name = product.name

        curr_product = get_product(product_code)
        source_product = curr_product.get_data()

        if source_product != None:

            product_version = source_product["version"] + 1

            product_data = ProductData(product_code, product_name, None, product_version)

            repo_update_product_name(product_data)

            response_message = "Product updated successfully."
        else:
            response_message = "No Product code found."
    except Exception as e:
        print(e)
        response_message = "Error fetching product."
    
    return Service_Response(response_message, None)


def update_product_stock(productStock: ProductStock):
    response_message = ""

    curr_product = get_product(productStock.code)
    source_product = curr_product.get_data()
    
    if source_product != None:

        source_product_version = source_product['version']
        new_product_version = source_product_version + 1

        source_stock = source_product['stock']
        updated_stock = 0

        if productStock.mutator == 'ADD':
            updated_stock = source_stock + productStock.stock
        elif productStock.mutator == 'REM' and source_stock > productStock.stock:
            updated_stock = source_stock - productStock.stock
        else:
            updated_stock = source_stock
        
        product_code = source_product["code"]
        product_name = source_product["name"]
        product_stock = updated_stock
        product_version = new_product_version

        product_data = ProductData(product_code, product_name, product_stock, product_version)

        repo_update_product_stock(product_data)

        response_message = "Product stock updated successfully."
    
    else:
        response_message = "No Product code found."

    return Service_Response(response_message, None)

def get_product(code: int) -> Service_Response:
    service_response: Service_Response = Service_Response(None,None)
    try:
        response: Repo_Response = repo_get_product(code)
        product_data = response.get_all()
        resp_msg = product_data["message"]
        resp_data = product_data["data"]
        
        if resp_msg == RESP_CODES['OK'] and resp_data != None:
            service_response = Service_Response(RESP_CODES['OK'], resp_data)
        else:
            service_response = Service_Response(RESP_CODES['ERR'], None)
    except Exception as e:
        log.info(f"Error in retrieving record for {code} - {e}")
        service_response = Service_Response(RESP_CODES['ERR'], None)
        
    return service_response