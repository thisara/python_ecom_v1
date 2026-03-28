from api.utils._db_client import get_mongo_client, get_db_conn 
from api.models.product import ProductData

client = get_mongo_client()
db = get_db_conn(client)
COL_PRODUCT="product"

def update_product(productData:ProductData, session):
    print(productData.__dict__)
    col = db[COL_PRODUCT]
    result = col.update_one(
        { "code": productData.code},
        { "$set":{"stock": productData.stock, "version": productData.version}},
        session=session
    )
    return result