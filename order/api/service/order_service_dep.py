from api.repository.order_repository import repo_confirm_order_items, repo_create_order, repo_get_order, repo_reserve_order_number
from api.service.ext_product_service import confirm_product_items

def create_order_repo_dep():
    return repo_create_order

def confirm_product_item_service_dep():
    return confirm_product_items

def confirm_order_items_repo_dep():
    return repo_confirm_order_items

def get_order_repo_dep():
    return repo_get_order

def reserve_order_number_repo_dep():
    return repo_reserve_order_number