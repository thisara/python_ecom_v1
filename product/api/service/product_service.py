import json
from pymongo import MongoClient
from pymongo.collection import Collection

from api.models.product import ProductData

from api.dto.product import Product, ProductOrderItem, ProductStock, ProductResponse

from collections import namedtuple
from json import JSONEncoder

from api.repository.product_repository import repo_create_product, repo_update_product_name, repo_update_product_stock, repo_get_product

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
        product_data = ProductData(product.code, product.name, __INIT_STOCK, __INIT_VERSION)
        
        repo_create_product(product_data)

        response_message = "Product created successfully."
    except Exception as e:
        response_message = "Error creating product."
    
    return ProductResponse(response_message)

def update_product_name(product: Product):
    response_message = ""
    try:
        product_code = product.code
        product_name = product.name

        source_product = get_product(product_code)
        
        product_version = source_product["version"] + 1
        
        if source_product != None:

            product_data = ProductData(product_code, product_name, None, product_version)

            repo_update_product_name(product_data)

            response_message = "Product updated successfully."
        else:
            response_message = "No Product code found."
    except Exception as e:
        response_message = "Error fetching product."
    
    return response_message


def update_product_stock(productStock: ProductStock):
    response_message = ""

    source_product = get_product(productStock.code)
    
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

    return ProductResponse(response_message)

def get_product(code: int):
    try:
        response = repo_get_product(code)
        product_data = response.data
        if product_data != None:
            return __id_serialiser(product_data)
        else:
            return None
    except Exception as e:
        print(e)
        return None #change to ProductResponse
