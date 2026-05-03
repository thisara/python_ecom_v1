from fastapi import APIRouter, Depends, HTTPException
from api.dto.order import OrderRequest, Client_Message_Response
from api.service.order_service import create_order, get_order, reserve_order_number
from api.utils.resp_codes import resp_codes, ERR, DUP, OK
from api.utils.app_logger import logger

log = logger(__name__)
RESP_CODES=resp_codes()
router = APIRouter()

@router.post("/", tags=["order"])
def create_order_endpoint(orderRequest: OrderRequest):
    
    try:
        response = create_order(orderRequest)
    except Exception as e:
        log.warning(f"Error creating order : {e}")
        raise #HTTPException(status_code=500, detail=f"Error creating order.")

    response_code = getattr(response, "message", None)

    if response_code == RESP_CODES[OK]:
        return Client_Message_Response(f"Order created!")
    if response_code == RESP_CODES[DUP]:
        return Client_Message_Response(f"Order already created!")

    log.warning(f"Something wrong creating the order!")            
    return HTTPException(status_code=400, detail=f"Something wrong creating order!")

@router.get("/{order_number}")
def get_order_endpoint(order_number: str):
    response = get_order(order_number)
    data = getattr(response, "data", None)

    if data is not None:
        return data

    return HTTPException(status_code=404, detail=f"Order not found!")

@router.post("/reserve-number")
def reserve_order_number_endpoint():
    response = reserve_order_number()
    data = getattr(response, "data", None)

    if data is not None:
        return data

    return HTTPException(status_code=404, detail=f"Order number not created!")