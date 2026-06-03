"""
User Model - Pydantic models for user-related operations
"""
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    """Base user model with common fields"""
    name: str = Field(..., min_length=1, max_length=200, description="User's full name")
    email: EmailStr = Field(..., description="User's email address")
    phone: str = Field(..., min_length=10, max_length=15, description="User's phone number")
    address: str = Field(..., min_length=5, description="User's delivery address")


class UserCreate(UserBase):
    """Model for creating a new user"""
    password: str = Field(..., min_length=6, description="User's password (min 6 characters)")


class UserUpdate(BaseModel):
    """Model for updating user information"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    phone: Optional[str] = Field(None, min_length=10, max_length=15)
    address: Optional[str] = Field(None, min_length=5)
    email: Optional[EmailStr] = None


class UserInDB(UserBase):
    """Model for user data as stored in the database"""
    id: str = Field(..., alias="_id", description="MongoDB document ID")
    password: str = Field(..., description="Hashed password")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True


class UserResponse(UserBase):
    """Model for user data returned in API responses"""
    id: str = Field(..., description="User ID")
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """Model for user login request"""
    email: EmailStr = Field(..., description="User's email")
    password: str = Field(..., min_length=6, description="User's password")


class TokenResponse(BaseModel):
    """Model for authentication token response"""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    user: UserResponse = Field(..., description="User information")
