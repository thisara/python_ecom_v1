from api.utils._db_client import DBConnection
from api.models.product import ProductOderItemData
from api.dto.product import Repo_Response
from api.utils.app_logger import logger

log = logger(__name__)
#from pymongo.collection import Collection
#from pymongo import MongoClient

#client = get_mongo_client()
#db = get_db_conn(client)
COL_PRODUCT_ITEM="product_order_item"

def repo_create_product_item(prodcutOrderItemData:ProductOderItemData, client = None, session = None):
    result: Repo_Response = Repo_Response(None, None)
    try:
        #col = db[COL_PRODUCT_ITEM]
        db_connection = DBConnection(client)
        col = db_connection.get_collection(COL_PRODUCT_ITEM)
        #col = _get_db_conn(COL_PRODUCT_ITEM, client)
        data = prodcutOrderItemData.__dict__.copy()

        if not data:
            log.warning("Error in data!")
            result = Repo_Response("Error in item data", {})
        else:
            db_response = col.insert_one(data, session=session)
            log.info("Added successfully!")
            result = Repo_Response("Added successfully", {str(db_response.inserted_id)})
    except Exception as e:
        print(e)

    return result
