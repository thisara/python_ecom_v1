from api.dto.product import Service_Response
from api.service.product_service_dep import get_product_fetcher, update_product_repo

def fake_get_product(code):
    return {"data":{"code": 1016,
                    "name": "Machien",
                    "stock": 38,
                    "version": 93}}

def fake_update_product(data):
    return Service_Response(RESP_CODES['OK'], None)

app.dependency_overrides[get_product_fetcher] = lambda: fake_get_product
app.dependency_overrides[update_product_repo] = lambda: fake_update_product