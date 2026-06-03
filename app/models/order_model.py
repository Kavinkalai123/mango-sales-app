"""
Order Model - Pydantic models for order-related operations
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum


class OrderStatus(str, Enum):
    """Enumeration of possible order statuses"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class PaymentMethod(str, Enum):
    """Enumeration of payment methods"""
    CASH_ON_DELIVERY = "cash_on_delivery"
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    UPI = "upi"
    WALLET = "wallet"


class OrderItemBase(BaseModel):
    """Base order item model"""
    product_id: str = Field(..., description="MongoDB product ID")
    quantity: int = Field(..., gt=0, description="Quantity in kg")
    price_per_kg: float = Field(..., gt=0, description="Price per kg at time of order")


class OrderItemCreate(OrderItemBase):
    """Model for creating order items"""
    pass


class OrderItemInDB(OrderItemBase):
    """Model for order item data in database"""
    id: str = Field(..., alias="_id")
    product_name: str = Field(..., description="Product name snapshot")

    class Config:
        populate_by_name = True


class OrderItemResponse(OrderItemBase):
    """Model for order items in API responses"""
    id: str = Field(..., description="Order item ID")
    product_name: str = Field(..., description="Product name at time of order")
    subtotal: float = Field(..., description="Total price (quantity * price_per_kg)")

    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    """Base order model"""
    user_id: str = Field(..., description="MongoDB user ID")
    status: OrderStatus = Field(default=OrderStatus.PENDING, description="Order status")
    shipping_address: str = Field(..., min_length=5, description="Delivery address")
    payment_method: PaymentMethod = Field(default=PaymentMethod.CASH_ON_DELIVERY)
    notes: Optional[str] = Field(None, max_length=500, description="Special instructions")


class OrderCreate(BaseModel):
    """Model for creating a new order"""
    user_id: str = Field(..., description="MongoDB user ID")
    items: List[OrderItemCreate] = Field(..., min_items=1, description="Order items list")
    shipping_address: str = Field(..., min_length=5)
    payment_method: PaymentMethod = Field(default=PaymentMethod.CASH_ON_DELIVERY)
    notes: Optional[str] = Field(None, max_length=500)


class OrderUpdate(BaseModel):
    """Model for updating order information"""
    status: Optional[OrderStatus] = None
    notes: Optional[str] = Field(None, max_length=500)


class OrderInDB(OrderBase):
    """Model for order data as stored in database"""
    id: str = Field(..., alias="_id", description="MongoDB document ID")
    items: List[OrderItemInDB] = Field(..., description="Ordered items")
    total_amount: float = Field(..., description="Total order amount")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True


class OrderResponse(OrderBase):
    """Model for order data in API responses"""
    id: str = Field(..., description="Order ID")
    items: List[OrderItemResponse] = Field(..., description="Order items")
    total_amount: float = Field(..., description="Total order amount")
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class OrderStatusUpdate(BaseModel):
    """Model for updating only order status"""
    status: OrderStatus = Field(..., description="New order status")
