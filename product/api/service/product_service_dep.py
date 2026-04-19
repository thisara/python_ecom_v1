from fastapi import Depends
from api.service.product_service import get_product
from api.repository.product_repository import repo_update_product_desc, repo_create_product, repo_update_product_stock, repo_get_async_product

def get_product_fetcher():
    return get_product

def update_product_repo():
    return repo_update_product_desc

def create_product_repo():
    return repo_create_product

def update_product_stock_repo():
    return repo_update_product_stock

async def get_product_async_repo():
    return repo_get_async_product