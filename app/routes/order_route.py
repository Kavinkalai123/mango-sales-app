from fastapi import APIRouter, HTTPException, status
from app.config.database import get_database
from app.schema.order_schema import (
    OrderCreate,
    OrderUpdate,
    OrderResponse,
)
from app.controllers import order_controller
from typing import List

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("/", response_model=List[OrderResponse])
async def list_orders(skip: int = 0, limit: int = 100):
    db = get_database()
    return await order_controller.get_orders(db, skip=skip, limit=limit)


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: str):
    db = get_database()
    order = await order_controller.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderCreate):
    db = get_database()
    try:
        return await order_controller.create_order(db, order)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{order_id}/status", response_model=OrderResponse)
async def update_order_status(order_id: str, order: OrderUpdate):
    db = get_database()
    updated_order = await order_controller.update_order_status(db, order_id, order.status)
    if not updated_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated_order


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(order_id: str):
    db = get_database()
    success = await order_controller.delete_order(db, order_id)
    if not success:
        raise HTTPException(status_code=404, detail="Order not found")