from typing import Callable
from datetime import datetime, timezone

from api.utils.db_tools import get_collection, get_client
from api.utils.app_logger import logger
from api.utils.resp_codes import resp_codes
from api.utils.constants import INIT_STATE

from api.models.product import ProductData, ProductStockData, ProductOderItemData
from api.dto.product import Product, ProductOrderItem, Repo_Response

from api.repository.product_item_repository import repo_create_product_item
from api.repository.product_repository import repo_update_product_stock

RESP_CODES=resp_codes()
log = logger(__name__)

def product_order_reservation(
    product_data: ProductData, 
    prod_odr_itm: ProductOrderItem,
    repo_update_stock_fn: Callable,
    repo_update_product_item_fn: Callable) -> Repo_Response:

    try:
        client = get_client()
        
        product_code = product_data.code
        product_name = product_data.name
        curr_product_version = product_data.version
        curr_product_stock = product_data.stock

        if curr_product_version == prod_odr_itm.version:
            
                with client.start_session() as session:

                    new_product_version = curr_product_version + 1
                    new_product_stock = curr_product_stock - prod_odr_itm.stock
                    
                    tx_time = datetime.now(timezone.utc)

                    productStockData = ProductStockData(
                        product_code,
                        new_product_stock,
                        new_product_version,
                        tx_time
                    )
                    
                    with session.start_transaction():    

                        product_order_item_data = ProductOderItemData(
                            prod_odr_itm.code, 
                            prod_odr_itm.stock, 
                            prod_odr_itm.orderRef, 
                            new_product_version,
                            tx_time,
                            tx_time,
                            INIT_STATE
                        )
                        
                        repo_update_stock_fn(productStockData, session)
                        repo_update_product_item_fn(product_order_item_data, session)
                        
                        session.commit_transaction()
                        session.end_session()

                        return Repo_Response(RESP_CODES['OK'], None)
        else:
            log.warning(f"Stale version of product code {product_code}")
            return Repo_Response(RESP_CODES['VER'], None)

    except Exception as e:
        log.warning(f"Error reserving items for order : {e}")
        raise
