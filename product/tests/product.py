from api.dto.product import ProductStock, ProductOrderItem
from api.service.product_service import update_product_desc,create_product,update_product_stock,get_async_product
from api.service.product_item_service import create_product_order_item
from api.models.product import ProductDescData, ProductData
from api.utils.resp_codes import resp_codes
from .mocks.product import fake_get_product,fake_async_get_product,fake_get_empty_product,fake_update_product_desc,fake_update_empty_product_desc,fake_update_product_stock,fake_update_empty_product_stock,fake_create_product
from .mocks.product_item import fake_update_product_item

RESP_CODES=resp_codes()

def test_create_product_success():

    result = create_product(
        productData=ProductData("1087", "Test Product 3", None, None),
        get_product_fn=fake_get_empty_product,
        repo_create_fn=fake_create_product
    )
    assert result.message == RESP_CODES['OK']

def test_create_product_exist():

    result = create_product(
        productData=ProductData(code=1087, name="Test Product 3", stock=None, version=None),
        get_product_fn=fake_get_product,
        repo_create_fn=fake_create_product
    )
    assert result.message == RESP_CODES['DUP']

def test_update_product_desc_success():

    result = update_product_desc(
        productDescData=ProductDescData(code=1001, name="Test Product 2", version=93),
        get_product_fn=fake_get_product,
        repo_update_fn=fake_update_product_desc
    )
    assert result.message == RESP_CODES['OK']

def test_update_product_desc_no_product():

    result = update_product_desc(
        productDescData=ProductDescData(code=1001, name="Test Product 2", version=93),
        get_product_fn=fake_get_empty_product,
        repo_update_fn=fake_update_empty_product_desc
    )
    assert result.message == RESP_CODES['NO_PROD_DATA']

def test_update_product_stock_success():

    result = update_product_stock(
        productStock=ProductStock(code=1001, stock=10, mutator="ADD"),
        get_product_fn=fake_get_product,
        repo_update_stock_fn=fake_update_product_stock
    )
    assert result.message == RESP_CODES['OK']


def test_update_product_stock_no_product_data():

    result = update_product_stock(
        productStock=ProductStock(code=1001, stock=10, mutator="ADD"),
        get_product_fn=fake_get_empty_product,
        repo_update_stock_fn=fake_update_empty_product_stock
    )
    assert result.message == RESP_CODES['NO_PROD_DATA']

def test_update_product_stock_invalid_mutator():

    result = update_product_stock(
        productStock=ProductStock(code=1001, stock=10, mutator="ADDS"),
        get_product_fn=fake_get_product,
        repo_update_stock_fn=fake_update_empty_product_stock
    )
    assert result.message == RESP_CODES['ERR']

async def test_get_async_product_success():

    result = await get_async_product(
        1001,
        get_product_async_fn=fake_async_get_product
    )
    assert result.data != None

"""
def test_product_order_reservation_success():

    result = create_product_order_item(
        productOrderItem=ProductOrderItem(code=1001, stock=1, orderRef=105, version=93),
        get_product_fn=fake_get_product,
        repo_update_stock_fn=fake_update_product_stock,
        repo_update_product_item_fn=fake_update_product_item
    )
    assert result.message == RESP_CODES['OK']
    """