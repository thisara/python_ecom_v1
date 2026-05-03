from typing import Callable
from datetime import datetime, timezone
import shortuuid

from api.utils.db_tools import get_collection, get_client
from api.utils.app_logger import logger
from api.utils.resp_codes import resp_codes, VER, OK
from api.utils.constants import INIT_STATE, INIT_VERSION, INIT_STATUS

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

                    #Move out from session
                    new_product_version = curr_product_version + 1
                    new_product_stock = curr_product_stock - prod_odr_itm.stock
                    
                    tx_time = datetime.now(timezone.utc)
                    order_item_id = shortuuid.uuid()

                    productStockData = ProductStockData(
                        code=product_code,
                        stock=new_product_stock,
                        version=new_product_version,
                        date_updated=tx_time
                    )
                    
                    with session.start_transaction():    

                        product_order_item_data = ProductOderItemData(
                            order_item_id=order_item_id,
                            code=prod_odr_itm.code, 
                            stock=prod_odr_itm.stock, 
                            orderRef=prod_odr_itm.orderRef, 
                            version=new_product_version,
                            status=INIT_STATUS,
                            date_created=tx_time,
                            date_updated=tx_time,
                            is_active=INIT_STATE
                        )
                        
                        repo_update_stock_fn(productStockData, session)
                        #change function name to create
                        repo_update_product_item_fn(product_order_item_data, session)
                        
                        session.commit_transaction()
                        session.end_session()

                        return Repo_Response(RESP_CODES[OK], None)
        else:
            log.warning(f"Stale version of product code {product_code}")
            return Repo_Response(RESP_CODES[VER], None)

    except Exception as e:
        log.warning(f"Error reserving items for order : {e}")
        raise
