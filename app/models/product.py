"""
Product data models and schemas
"""
from typing import List, Optional
from pydantic import BaseModel, Field, GetCoreSchemaHandler
from pydantic_core import core_schema
from bson import ObjectId


class PyObjectId(ObjectId):
    """Custom ObjectId support for Pydantic v2"""

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: type, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_plain_validator_function(cls.validate)

    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return v
        if isinstance(v, str) and ObjectId.is_valid(v):
            return ObjectId(v)
        raise TypeError("Invalid ObjectId")


class Size(BaseModel):
    """Product size model"""
    size: str = Field(..., description="Size name")
    quantity: int = Field(..., ge=0, description="Available quantity")


class ProductCreate(BaseModel):
    """Product creation schema"""
    name: str = Field(..., min_length=1, max_length=200, description="Product name")
    price: float = Field(..., gt=0, description="Product price")
    sizes: List[Size] = Field(..., description="Available sizes and quantities")


class ProductResponse(BaseModel):
    """Product response schema"""
    id: str = Field(..., description="Product ID")
    name: str = Field(..., description="Product name")
    price: float = Field(..., description="Product price")


class ProductListResponse(BaseModel):
    """Product list response schema"""
    data: List[ProductResponse]
    page: dict


class ProductInDB(BaseModel):
    """Product database model"""
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    price: float
    sizes: List[Size]

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
