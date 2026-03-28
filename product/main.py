from fastapi import FastAPI
#from pydantic import BaseModel, field_validator, validator
#import service
#import serviceProductItem

#from product import Product, ProductOrderItem, ProductStock

#import json
from api.v1.router import api_router

app = FastAPI()

app.include_router(api_router, prefix="/product")

"""
__mutators = ['ADD', 'REM']

@app.post("/product")
def create_product(product: Product):
    existing_product = service.get_product(product.code)
    if existing_product != None:
        return {"message": "Product already exist!"}
    else:
        message = service.create_product(product)
        return message

@app.get("/product/{code}")
async def get_product(code: int):
    product = service.get_product(code)
    if product != None:
        return product
    else:
        return "No Product Found!"

@app.put("/product")
def update_product(product: Product):
    if product != None:
        status = service.update_product(product)
        return status
    else:
        return "No Product Found"

@app.put("/product/order/stock")
def reserve_product_order_stock(productOrderItem: ProductOrderItem):
    if productOrderItem != None and productOrderItem.code >= 1000:
        response = serviceProductItem.create_product_order_item(productOrderItem)
        return response
    else:
        return "No Product Found!"


@app.put("/product/stock")
def update_product_stock(productStock: ProductStock):
    if productStock != None and productStock.code >= 1000 and productStock.mutator in __mutators:
        status = service.update_product_stock(productStock)
        return status
    else:
        return "Invalid product stock data!"

"""