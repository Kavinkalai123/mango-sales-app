"""
Product Model - Pydantic models for product-related operations
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ProductBase(BaseModel):
    """Base product model with common fields"""
    name: str = Field(..., min_length=1, max_length=200, description="Product name (e.g., Mango)")
    variety: str = Field(..., min_length=1, max_length=100, description="Product variety (e.g., Alphonso, Kesar)")
    description: Optional[str] = Field(None, max_length=1000, description="Product description")
    price_per_kg: float = Field(..., gt=0, description="Price per kilogram")
    stock_quantity: int = Field(default=0, ge=0, description="Available stock in kg")
    image_url: Optional[str] = Field(None, description="URL to product image")
    is_active: bool = Field(default=True, description="Whether product is active/available")


class ProductCreate(ProductBase):
    """Model for creating a new product"""
    pass


class ProductUpdate(BaseModel):
    """Model for updating product information"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    variety: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    price_per_kg: Optional[float] = Field(None, gt=0)
    stock_quantity: Optional[int] = Field(None, ge=0)
    image_url: Optional[str] = None
    is_active: Optional[bool] = None


class ProductInDB(ProductBase):
    """Model for product data as stored in the database"""
    id: str = Field(..., alias="_id", description="MongoDB document ID")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True


class ProductResponse(ProductBase):
    """Model for product data returned in API responses"""
    id: str = Field(..., description="Product ID")
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProductBrief(BaseModel):
    """Brief product info for order items"""
    id: str = Field(..., description="Product ID")
    name: str = Field(..., description="Product name")
    variety: str = Field(..., description="Product variety")
    price_per_kg: float = Field(..., description="Price per kg at time of order")
