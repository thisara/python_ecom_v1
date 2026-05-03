from fastapi import Depends
from api.repository.product_item_repository import repo_create_product_item, repo_get_product_order_item, repo_confirm_product_order_items

def create_product_item_dep():
    return repo_create_product_item

def confirm_product_item_dep():
    return repo_confirm_product_order_items

def get_product_item_stock_dep():
    return repo_get_product_order_item