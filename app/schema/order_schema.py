from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class OrderItemBase(BaseModel):
    product_id: str
    quantity: int
    price_per_kg: float


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemResponse(OrderItemBase):
    product_name: Optional[str] = None
    subtotal: float


class OrderBase(BaseModel):
    user_id: str
    total_amount: float
    status: str = "pending"


class OrderCreate(BaseModel):
    user_id: str
    items: List[OrderItemCreate]


class OrderUpdate(BaseModel):
    status: Optional[str] = None


class OrderResponse(OrderBase):
    id: str
    created_at: Optional[datetime] = None
    items: List[OrderItemResponse] = []

    class Config:
        from_attributes = True