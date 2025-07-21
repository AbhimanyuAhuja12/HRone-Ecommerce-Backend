"""
Order API endpoints
"""
import logging
from fastapi import APIRouter, Query, Path, status

from app.services.order_service import OrderService
from app.models.order import OrderCreate, OrderListResponse
from app.core.config import settings

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/orders", status_code=status.HTTP_201_CREATED)
async def create_order(order_data: OrderCreate):
    """
    Create a new order
    
    - **userId**: User ID placing the order
    - **items**: List of products and quantities to order
    """
    try:
        service = OrderService()
        result = await service.create_order(order_data)
        logger.info(f"Order created successfully: {result['id']}")
        return result
    except Exception as e:
        logger.error(f"Failed to create order: {e}")
        raise


@router.get("/orders/{user_id}", response_model=OrderListResponse)
async def get_user_orders(
    user_id: str = Path(..., description="User ID to get orders for"),
    limit: int = Query(settings.DEFAULT_PAGE_SIZE, ge=1, le=settings.MAX_PAGE_SIZE, description="Number of orders to return"),
    offset: int = Query(0, ge=0, description="Number of orders to skip")
):
    """
    Get orders for a specific user with pagination
    
    - **user_id**: User ID to retrieve orders for
    - **limit**: Number of orders to return (1-100)
    - **offset**: Number of orders to skip for pagination
    """
    try:
        service = OrderService()
        result = await service.get_user_orders(
            user_id=user_id,
            limit=limit,
            offset=offset
        )
        logger.info(f"Retrieved {len(result['data'])} orders for user {user_id}")
        return result
    except Exception as e:
        logger.error(f"Failed to get orders for user {user_id}: {e}")
        raise
