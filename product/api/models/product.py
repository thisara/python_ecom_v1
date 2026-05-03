from dataclasses import dataclass
from typing import Optional, List

@dataclass
class ProductData():
    code: str
    name: str
    stock: float
    version: int
    date_created: Optional[str] = None 
    date_updated: Optional[str] = None 
    is_active: Optional[str] = True 

@dataclass
class ProductDescData():
    code: str
    name: str
    version: int
    date_updated: Optional[str] = None 

@dataclass
class ProductStockData():
    code: str
    stock: float
    version: int
    date_updated: Optional[str] = None 

@dataclass
class ClientProductData():
    code: str
    name: str
    stock: float
    version: int

@dataclass
class ProductOderItemData():
    order_item_id: str
    code: str
    stock: float
    orderRef: str
    version: int
    status: Optional[str] = None
    date_created: Optional[str] = None 
    date_updated: Optional[str] = None 
    is_active: Optional[str] = True 

@dataclass
class ProductOrderData():
    order_number: str
    product_items: List[ProductOderItemData]


@dataclass
class OrderLineItemConfirm():
    code: int
    stock: float
    version: int
    status: str

@dataclass
class OrderConfirmedData():
    order_number: str
    status: str
    confirmed_items: List[OrderLineItemConfirm]