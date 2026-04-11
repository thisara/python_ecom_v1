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

@dataclass
class ProductStockData():
    code: str
    stock: float
    version: int

@dataclass
class ClientProductData():
    code: str
    name: str
    stock: float
    version: int

"""
    def __init__(self, code, name, stock, version):
        self.code = code
        self.name = name
        self.stock = stock
        self.version = version
"""
class ProductOderItemData():
    def __init__(self, code, stock, orderRef, version):
        self.code = code
        self.stock = stock
        self.orderRef = orderRef
        self.version = version


