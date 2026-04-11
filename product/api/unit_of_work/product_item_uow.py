from api.utils._db_client import DBConnection

from api.models.product import ProductData, ProductOderItemData
from api.dto.product import Product, ProductOrderItem, Repo_Response

from api.repository.product_item_repository import repo_create_product_item
from api.repository.product_repository import repo_update_product
from api.utils._message import get_global_messages
from api.utils.app_logger import logger
from api.utils.resp_codes import resp_codes

RESP_CODES=resp_codes()
log = logger(__name__)

def product_order_reservation(product: Product, productOrderItem: ProductOrderItem) -> str:

    try:
        db_connection = DBConnection()
        client = db_connection.get_client()

        product_code = product.code
        product_name = product.name
        curr_product_version = product.version
        curr_product_stock = product.stock

        global_messages = get_global_messages()

        if curr_product_version == productOrderItem.version:
            
                with client.start_session() as session:

                    new_product_version = curr_product_version + 1
                    new_product_stock = curr_product_stock - productOrderItem.stock
                    productData = ProductData(product_code,product_name,new_product_stock,new_product_version)
                    
                    with session.start_transaction():    

                        product_order_item_data = ProductOderItemData(productOrderItem.code, productOrderItem.stock, productOrderItem.orderRef, new_product_version)
                        
                        repo_update_product(productData, client, session)
                        repo_create_product_item(product_order_item_data, client, session)
                        
                        session.commit_transaction()
                        session.end_session()

                        return Repo_Response(RESP_CODES['OK'], None)
        else:
            log.warning(f"Low stock available for product code {prod_code}")
            return Repo_Response(RESP_CODES['LOW'], None)

    except Exception as e:
        log.warning(f"Error reserving items for order : {e}")
        raise e
    finally:
        #check for active sessions!
        if session is not None:
            session.end_session()
        if client is not None:
            client.close()