from api.dto.product import Product
from api.models.product import ProductData, ProductDescData, ClientProductData

def to_product_data(product: Product) -> ProductData:
    if not product:
        return None

    return ProductData(
        code=product.code,
        name=product.name,
        stock=_get_object_attr(product, 'stock'),
        version=_get_object_attr(product, 'version')
    )

def to_product_desc_data(product: Product) -> ProductData:
    if not product:
        return None

    return ProductDescData(
        code=product.code,
        name=product.name,
        version=_get_object_attr(product, 'version')
    )

def to_client_product_data(data: ProductData):
    if not data:
        return None
    
    return ClientProductData(
        code=data.code,
        name=data.name,
        stock=data.stock,
        version=data.version
    )

def _get_object_attr(object, value):
    if hasattr(object, value):
        return object.value
    else:
        return None