"""
Main API router
"""
from fastapi import APIRouter

from app.api.v1.endpoints import products, orders

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(products.router, tags=["products"])
api_router.include_router(orders.router, tags=["orders"])
