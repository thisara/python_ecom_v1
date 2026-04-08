from pydantic import BaseModel, field_validator

class Product(BaseModel):
    #model_config = ConfigDict(extra='allow')
    code: int
    name: str

    @field_validator("code", mode="before")
    @classmethod
    def validate_code(cls, value):
        if value == None:
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

class ProductOrderItem(BaseModel):
    code: int
    stock: float
    orderRef: int

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