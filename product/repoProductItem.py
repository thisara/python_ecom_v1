"""
from api.utils._db_client import get_mongo_client, get_db_conn 
from product import ProductOderItemData

client = get_mongo_client()
db = get_db_conn(client)
COL_PRODUCT_ITEM="product_order_item"

def create_product_item(product_order_item_data:ProductOderItemData, session):
    col = db[COL_PRODUCT_ITEM]
    result = col.insert_one(product_order_item_data.__dict__, session=session)
    return result
"""