from api.utils.db_tools import get_collection, get_collection_names
from api.models.product import ProductOderItemData
from api.dto.product import Repo_Response
from dataclasses import asdict
from api.utils.app_logger import logger

log = logger(__name__)
COL_PRODUCT_ITEM=get_collection_names().get('PRODUCT_ITEM')

def repo_create_product_item(prodcutOrderItemData:ProductOderItemData, client = None, session = None):
    try:
        col = get_collection(COL_PRODUCT_ITEM)
        data = asdict(prodcutOrderItemData)

        if not data:
            log.warning("Error in data!")
            return Repo_Response("Error in item data", {})
 
        db_response = col.insert_one(data, session=session)
        log.info("Added successfully!")
        return Repo_Response("Added successfully", {str(db_response.inserted_id)})
    
    except Exception as e:
        log.warning("Error creating product item!")
        raise
