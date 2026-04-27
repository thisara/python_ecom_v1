from pydantic import BaseModel, field_validator
from typing import List

class ProductItem(BaseModel):
    line_id: int
    product_code: int
    quantity: float
    version: int

    @field_validator("line_id", mode="before")
    @classmethod
    def validate_line_id(cls, value):
        if value is None:
            raise ValueError("Line ID is required!")
        if value <= 0:
            raise ValueError("Line ID must be a positive integer!")
        return value

    @field_validator("product_code", mode="before")
    @classmethod
    def validate_code(cls, value):
        if value is None:
            raise ValueError("Prodcut code is required!")
        if value <= 0:
            raise ValueError("Prodcut code must be a positive integer!")
        if value <= 1000 or value >= 9999:
            raise ValueError("code must be between 1000 and 9999!")
        return value

    @field_validator("quantity", mode="before")
    @classmethod
    def validate_stock(cls, value):
        if value is None:
            raise ValueError("Stock value requred!")
        if not isinstance(float(value), float):
            raise ValueError("Stock has to be a number!")
        return value

    @field_validator("version", mode="before")
    @classmethod
    def validate_version(cls, value):
        if value is None:
            raise ValueError("Version value requred!")
        if value < 0 :
            raise ValueError("Version has to be a positive number!")
        return value


class OrderRequest(BaseModel):
    order_number: str
    order_items: List[ProductItem]

    @field_validator("order_number", mode="before")
    @classmethod
    def validate_id(cls, value):
        if value is None:
            raise ValueError("Order ID is required!")
        if len(value) != 36:
            raise ValueError("Order ID should be a valid GUID!")
        return value

    @field_validator("order_items", mode="before")
    @classmethod
    def validate_order_items(cls, value):
        if value is None:
            raise ValueError("Order item is required!")
        if len(value) == 0:
            raise ValueError("Order items cannot be empty!")
        if len({v["line_id"] for v in value}) != len(value):
            raise ValueError("Line ID should be unique!")
        return value 

class Client_Message_Response():
    def __init__(self, message: str):
        self.message = message
    def get_message(self):
        return self.message

class Repo_Response():
    def __init__(self, message: str, data: dict):
        self.message = message
        self.data = data

    def get_message(self):
        return self.message

    def get_data(self):
        return self.data

    def get_all(self):
        return {
            "message": self.message,
            "data": self.data
        }

class Service_Response():
    def __init__(self, message: str, data: dict):
        self.message = message
        self.data = data

    def get_message(self):
        return self.message

    def get_data(self):
        return self.data

    def get_all(self):
        return {
            "message": self.message,
            "data": self.data
        }