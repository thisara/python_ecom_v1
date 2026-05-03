from dataclasses import dataclass
from typing import Optional
from typing import List

@dataclass
class OrderItemData():
    line_id: int
    prod_code: int
    quantity: float
    status: int
    version: int
    date_created: Optional[str] = None 
    date_updated: Optional[str] = None 
    is_active: Optional[str] = True 

@dataclass
class OrderData():
    order_number: str
    order_items: List[OrderItemData]
    version: int
    status: str
    date_created: Optional[str] = None 
    date_updated: Optional[str] = None 
    is_active: Optional[str] = True 

@dataclass
class OrderNumber():
    order_number: str
    version: int
    status: str
    date_created: Optional[str] = None 
    date_updated: Optional[str] = None 
    is_active: Optional[str] = True 

#---API Contracts

@dataclass
class OrderLineItemConfirm():
    code: int
    stock: float
    version: int

@dataclass
class OrderItemConfirm():
    orderRefernce: str
    productItems: List[OrderLineItemConfirm]
    