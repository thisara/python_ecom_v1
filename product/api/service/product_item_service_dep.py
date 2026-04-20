from fastapi import Depends
from api.repository.product_item_repository import repo_create_product_item

def update_product_item_stock_dep():
    return repo_create_product_item