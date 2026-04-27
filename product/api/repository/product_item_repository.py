from api.utils.db_tools import get_collection, get_collection_names
from api.models.product import ProductOderItemData
from api.dto.product import Repo_Response
from dataclasses import asdict
from api.utils.resp_codes import resp_codes, OK, ERR
from api.utils.app_logger import logger

log = logger(__name__)
RESP_CODES=resp_codes()
COL_PRODUCT_ITEM=get_collection_names().get('PRODUCT_ITEM')

def repo_create_product_item(prodcutOrderItemData:ProductOderItemData, session = None) -> Repo_Response:
    try:
        col = get_collection(COL_PRODUCT_ITEM)
        data = asdict(prodcutOrderItemData)

        if not data:
            log.warning("Error in data!")
            return Repo_Response(RESP_CODES[ERR], {})
 
        db_response = col.insert_one(data, session=session)
        log.info("Added successfully!")
        return Repo_Response(RESP_CODES[OK], {str(db_response.inserted_id)})
    
    except Exception as e:
        log.warning("Error creating product item!")
        raise
