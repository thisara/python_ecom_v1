"""
import json
from pymongo import MongoClient
from pymongo.collection import Collection
from product import Product, ProductData, ProductOrderItem, ProductStock, ProductResponse
from collections import namedtuple
from json import JSONEncoder

MONGO_URL = "mongodb://127.0.0.1:27017/?replicaSet=rs01"
DB_NAME = "order_db"
COLLECTION_NAME = "product"

__INIT_VERSION = 0
__INIT_STOCK = 0

def __get_db_conn() -> Collection:
    client = MongoClient(MONGO_URL)
    db = client[DB_NAME]
    col = db[COLLECTION_NAME]
    return col


def __id_serialiser(object)-> dict:
    #object["id"] = str(object["_id"])
    del object["_id"]
    return object


def create_product(product: Product):
    response_message = ""
    try:
        prod_col = __get_db_conn()
        product_data = ProductData(product.code, product.name, __INIT_STOCK, __INIT_VERSION)
        prod_col.insert_one(product_data.__dict__)
        response_message = "Product created successfully."
    except Exception as e:
        response_message = "Error creating product."
    return ProductResponse(response_message)


def update_product(product: Product):
    response_message = ""
    try:
        prod_col = __get_db_conn()
        product_code = product.code
        source_product = get_product(product_code)
        if source_product != None:
            prod_col.update_one(
                { "code": source_product["code"]},
                { "$set":{"name": product.name}}
            )
            response_message = "Product updated successfully."
        else:
            response_message = "No Product code found."
    except:
        response_message = "Error fetching product."
    
    return response_message


def update_product_stock(productStock: ProductStock):
    response_message = ""
    prod_col = __get_db_conn()
    source_product = get_product(productStock.code)
    
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
    
    prod_col.update_one(
        { "code": source_product["code"]},
        { "$set":{"stock": updated_stock, "version": new_product_version}}
    )
    response_message = "Product stock updated successfully."
    return ProductResponse(response_message)

def get_product(code: int):
    try:
        prod_col = __get_db_conn()
        product = prod_col.find_one({"code": code})

        if product != None:
            return __id_serialiser(product)
        else:
            return None
    except:
        return None


#def __jsonDecoder(_dict):
#    return namedtuple('X', _dict.keys())(*_dict.values())

#def __toProductData(product: Product, version):
#    _product_data = ProductData(product['code'], product['name'], product['stock'], version)
#    return _product_data

#def __toProduct(product: Product):
#    _product = ProductData(product['code'], product['name'])
#    return _product

"""