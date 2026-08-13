from fastapi import APIRouter, status, HTTPException, Depends, Body
from app.schemas.order import OrderSchema
from app.services import order_service
from app.services.auth_service import get_current_user

router = APIRouter()

@router.post("/add", status_code=status.HTTP_201_CREATED)
def place_order(order: OrderSchema, current_user: dict = Depends(get_current_user)):
    user_id = int(current_user["id"])
    return order_service.create_order(user_id, order)

@router.get("/user", status_code=status.HTTP_200_OK)
def get_my_orders(current_user: dict = Depends(get_current_user)):
    user_id = int(current_user["id"])
    return order_service.get_user_orders(user_id)

@router.get("/all", status_code=status.HTTP_200_OK)
def get_all_orders(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return order_service.get_all_orders()

@router.put("/{order_id}/status", status_code=status.HTTP_200_OK)
def update_status(order_id: str, status_update: str = Body(..., alias="status", embed=True), current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
        
    if not status_update:
        raise HTTPException(status_code=400, detail="Status field is required")
        
    try:
        updated_order = order_service.update_order_status(order_id, status_update)
        if not updated_order:
            raise HTTPException(status_code=404, detail="Order not found")
        return updated_order
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
