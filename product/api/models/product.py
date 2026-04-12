from dataclasses import dataclass
from typing import Optional

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
    code: str
    stock: float
    orderRef: str
    version: int
    date_created: Optional[str] = None 
    date_updated: Optional[str] = None 
    is_active: Optional[str] = True 
