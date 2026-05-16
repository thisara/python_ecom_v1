from fastapi import APIRouter, Depends, HTTPException, Request
from api.dto.order import OrderRequest, Client_Message_Response
from api.service.order_service import create_order, get_order, reserve_order_number
from api.utils.resp_codes import NON, PAR, resp_codes, DUP, OK
from api.utils.app_logger import logger
from api.service.order_service_dep import confirm_order_items_repo_dep, confirm_product_item_service_dep, create_order_repo_dep, get_order_repo_dep, reserve_order_number_repo_dep

log = logger(__name__)
RESP_CODES=resp_codes()
router = APIRouter()

@router.post("/", tags=["order"])
async def create_order_endpoint(
    orderRequest: OrderRequest, 
    request: Request,
    get_order_fn=Depends(get_order_repo_dep),
    create_order_fn=Depends(create_order_repo_dep),
    confirm_product_items_fn=Depends(confirm_product_item_service_dep),
    confirm_order_items_fn=Depends(confirm_order_items_repo_dep)):
    
    try:
        response = await create_order(
            orderRequest, 
            request,
            get_order_fn=get_order_fn,
            repo_create_order_fn=create_order_fn,
            confirm_product_items_fn=confirm_product_items_fn,
            repo_confirm_order_items_fn=confirm_order_items_fn)
    except Exception as e:
        log.warning(f"Error creating order : {e}")
        raise HTTPException(status_code=500, detail=f"Error creating order.")

    response_code = getattr(response, "message", None)

    if response_code == RESP_CODES[OK]:
        return Client_Message_Response(f"Order created!")
    if response_code == RESP_CODES[NON]:
        return Client_Message_Response(f"Order created, no order items confimed!")
    if response_code == RESP_CODES[PAR]:
        return Client_Message_Response(f"Order created, partial order items confirmed!")
    if response_code == RESP_CODES[DUP]:
        return Client_Message_Response(f"Order already created!")

    log.warning(f"Something wrong creating the order!")            
    return HTTPException(status_code=400, detail=f"Something wrong creating order!")

@router.get("/{order_number}")
async def get_order_endpoint(
    order_number: str,
    get_order_repo_fn=Depends(get_order_repo_dep)):

    try:
        response = await get_order(
            order_number=order_number,
            get_order_repo_fn=get_order_repo_fn)
        
    except Exception as e:
        log.warning(f"Error fetching order : {e}")
        return HTTPException(status_code=400, detail=f"Error fetching order.!")

    data = getattr(response, "data", None)

    if data is not None:
        return HTTPException(status_code=200, detail=data)

    return HTTPException(status_code=404, detail=f"Order not found!")

@router.post("/reserve-number")
async def reserve_order_number_endpoint(
    reserve_order_number_repo_fn=Depends(reserve_order_number_repo_dep)):

    try:
        response = await reserve_order_number(
            reserve_order_number_repo_fn=reserve_order_number_repo_fn)
    except Exception as e:
        log.warning(f"Error generating order number : {e}")
        return HTTPException(status_code=400, detail=f"Error generating order number.!")
    
    data = getattr(response, "data", None)

    if data is not None:
        return data

    return HTTPException(status_code=404, detail=f"Order number not created!")