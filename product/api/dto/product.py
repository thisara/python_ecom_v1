from pydantic import BaseModel, field_validator

class Product(BaseModel):
    #model_config = ConfigDict(extra='allow')
    code: int
    name: str

    @field_validator("code", mode="before")
    @classmethod
    def validate_code(cls, value):
        if value <= 0:
            raise ValueError("code must be a positive integer")
        if value <= 1000 or value >= 9999:
            raise ValueError("code must be between 1000 and 9999")
        return value

    @field_validator("name", mode="before")
    @classmethod
    def validate_name(cls, value):
        if not value.strip():
            raise ValueError("name cannot be empty")
        if len(value) > 100:
            raise ValueError("name cannot exceed 100 characters")
        return value

class ProductStock(BaseModel):
    code: int
    stock: float
    mutator: str

class ProductOrderItem(BaseModel):
    code: int
    stock: float
    orderRef: int

class ProductResponse():
    def __init__(self, message):
        self.message = message