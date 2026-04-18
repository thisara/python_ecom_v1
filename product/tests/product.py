from api.dto.product import Service_Response
from api.service.product_service import update_product_desc
from api.models.product import ProductDescData, ProductData
from api.utils.resp_codes import resp_codes

RESP_CODES=resp_codes()

#ProductData(code=1016, name='Machien', stock=38.0, version=96, date_created=None, date_updated=None, is_active=True)

def fake_get_product(code):
    prodData = ProductData(code=str(1016),
                name='Machien',
                stock=38.0,
                version=93)
    return Service_Response(message=None, data=prodData)

def fake_update_product(data):
    return Service_Response(RESP_CODES['OK'], None)

def test_update_product_desc_success():

    result = update_product_desc(
        productDescData=ProductDescData("1016", "Machien", 93),
        get_product_fn=fake_get_product,
        repo_update_fn=fake_update_product
    )

    assert result.message == RESP_CODES['OK']