from api.models.product import ProductData

def to_product(data: dict) -> ProductData:
    if not data:
        return None
    
    return ProductData(
        code=data.get("code"),
        name=data.get("name"),
        stock=data.get("stock"),
        version=data.get("version")
    )
