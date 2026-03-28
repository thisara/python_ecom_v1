from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator, validator
import service

app = FastAPI()

class Order(BaseModel):
    order_number: str
    product: dict
    user: str

@app.post("/order")


@app.get("/order/{id}")