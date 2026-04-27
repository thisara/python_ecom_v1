from pydantic import BaseModel, field_validator

class Product(BaseModel):
    #model_config = ConfigDict(extra='allow')
    code: int
    name: str

    @field_validator("code", mode="before")
    @classmethod
    def validate_code(cls, value):
        if value is None:
            raise ValueError("Prodcut code is required!")
        if value <= 0:
            raise ValueError("Prodcut code must be a positive integer!")
        if value <= 1000 or value >= 9999:
            raise ValueError("code must be between 1000 and 9999!")
        return value

    @field_validator("name", mode="before")
    @classmethod
    def validate_name(cls, value):
        if not value.strip():
            raise ValueError("Product name cannot be empty!")
        if len(value) > 100:
            raise ValueError("Product name cannot exceed 100 characters!")
        return value

class ProductStock(BaseModel):
    code: int
    stock: float
    mutator: str

    @field_validator("code", mode="before")
    @classmethod
    def validate_code(cls, value):
        if value is None:
            raise ValueError("Prodcut code is required!")
        if value <= 0:
            raise ValueError("Prodcut code must be a positive integer!")
        if value <= 1000 or value >= 9999:
            raise ValueError("code must be between 1000 and 9999!")
        return value

    @field_validator("stock", mode="before")
    @classmethod
    def validate_stock(cls, value):
        if value is None:
            raise ValueError("Stock value requred!")
        if not isinstance(float(value), float):
            raise ValueError("Stock has to be a number!")
        return value

    #validate mutator
    #remove boilerplace code

class ProductOrderItem(BaseModel):
    code: int
    stock: float
    orderRef: int
    version: int

    @field_validator("code", mode="before")
    @classmethod
    def validate_code(cls, value):
        if value is None:
            raise ValueError("Prodcut code is required!")
        if value <= 0:
            raise ValueError("Prodcut code must be a positive integer!")
        if value <= 1000 or value >= 9999:
            raise ValueError("code must be between 1000 and 9999!")
        return value

    @field_validator("stock", mode="before")
    @classmethod
    def validate_stock(cls, value):
        if value is None:
            raise ValueError("Stock value requred!")
        if not isinstance(float(value), float):
            raise ValueError("Stock has to be a number!")
        return value

    @field_validator("orderRef", mode="before")
    @classmethod
    def validate_orderRef(cls, value):
        if value is None:
            raise ValueError("Order Reference is required!")
        if value <=0:
            raise ValueError("Order Reference should be a positive number!")
        if value <=100 or value >= 999:
            raise ValueError("Order Reference must be between 100 and 999!")
        return value

    @field_validator("version", mode="before")
    @classmethod
    def validate_version(cls, value):
        if value is None:
            raise ValueError("Version value requred!")
        if value < 0 :
            raise ValueError("Version has to be a positive number!")
        return value

#?? usage
class ProductResponse():
    def __init__(self, message):
        self.message = message

class Client_Data_Response():
    def __init__(self, data: dict):
        self.data = data
    def get_data(self):
        return self.data

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