from api.models.product import ProductOderItemData, ProductOrderData

def to_product_items(order_number: str, data: dict) -> ProductOrderData:
    if not data:
        return None
    
    items: ProductOderItemData = []

    for d in data:
        items.append(ProductOderItemData(
            order_item_id=d.get("order_item_id"),
            code=d.get("code"),
            orderRef=d.get("orderRef"),
            stock=d.get("stock"),
            version=d.get("version"),
            status=d.get("status"),
            date_created=d.get("date_created"),
            date_updated=d.get("date_updated"),
            is_active=d.get("is_active")))
    
    return ProductOrderData(
        order_number=order_number,
        product_items=items)

