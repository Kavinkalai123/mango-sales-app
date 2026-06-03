from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# Product Schemas
class ProductBase(BaseModel):
    name: str
    variety: str
    description: Optional[str] = None
    price_per_kg: float
    stock_quantity: int
    image_url: Optional[str] = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    variety: Optional[str] = None
    description: Optional[str] = None
    price_per_kg: Optional[float] = None
    stock_quantity: Optional[int] = None
    image_url: Optional[str] = None


class ProductResponse(ProductBase):
    id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True