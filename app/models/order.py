"""
Order data models and schemas
"""
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from bson import ObjectId

from app.models.product import PyObjectId


class OrderItem(BaseModel):
    """Order item schema"""
    productId: str = Field(..., description="Product ID")
    qty: int = Field(..., gt=0, description="Quantity")


class OrderCreate(BaseModel):
    """Order creation schema"""
    userId: str = Field(..., description="User ID")
    items: List[OrderItem] = Field(..., min_items=1, description="Order items")


class ProductDetails(BaseModel):
    """Product details for order response"""
    name: str = Field(..., description="Product name")
    id: str = Field(..., description="Product ID")


class OrderItemResponse(BaseModel):
    """Order item response schema"""
    productDetails: ProductDetails
    qty: int


class OrderResponse(BaseModel):
    """Order response schema"""
    id: str = Field(..., description="Order ID")
    items: List[OrderItemResponse]
    total: float = Field(..., description="Total order amount")


class OrderListResponse(BaseModel):
    """Order list response schema"""
    data: List[OrderResponse]
    page: dict


class OrderInDB(BaseModel):
    """Order database model"""
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    userId: str
    items: List[OrderItem]
    total: float
    createdAt: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
