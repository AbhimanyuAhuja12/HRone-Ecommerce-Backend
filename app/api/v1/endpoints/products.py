"""
Product API endpoints
"""
import logging
from typing import Optional
from fastapi import APIRouter, Query, status, HTTPException

from app.services.product_service import ProductService
from app.models.product import ProductCreate, ProductListResponse
from app.core.config import settings

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/products", status_code=status.HTTP_201_CREATED)
async def create_product(product_data: ProductCreate):
    """
    Create a new product
    
    - **name**: Product name (required)
    - **price**: Product price (required, must be positive)
    - **sizes**: List of available sizes with quantities
    """
    try:
        service = ProductService()
        result = await service.create_product(product_data)
        logger.info(f"Product created successfully: {result['id']}")
        return result
    except Exception as e:
        logger.error(f"Failed to create product: {e}")
        raise


@router.get("/products", response_model=ProductListResponse)
async def get_products(
    name: Optional[str] = Query(None, description="Filter by product name (supports partial search)"),
    size: Optional[str] = Query(None, description="Filter by available size"),
    limit: int = Query(settings.DEFAULT_PAGE_SIZE, ge=1, le=settings.MAX_PAGE_SIZE, description="Number of products to return"),
    offset: int = Query(0, ge=0, description="Number of products to skip")
):
    """
    Get products with optional filtering and pagination
    
    - **name**: Filter by product name (partial search supported)
    - **size**: Filter products that have this size available
    - **limit**: Number of products to return (1-100)
    - **offset**: Number of products to skip for pagination
    """
    try:
        service = ProductService()
        result = await service.get_products(
            name=name,
            size=size,
            limit=limit,
            offset=offset
        )
        logger.info(f"Retrieved {len(result['data'])} products")
        return result
    except Exception as e:
        logger.error(f"Failed to get products: {e}")
        raise
