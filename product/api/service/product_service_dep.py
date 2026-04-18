from fastapi import Depends
from api.service.product_service import get_product
from api.repository.product_repository import repo_update_product_desc

def get_product_fetcher():
    return get_product

def update_product_repo():
    return repo_update_product_desc


