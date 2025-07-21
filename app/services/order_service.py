"""
Order business logic service
"""
import logging
from typing import Dict, Any

from app.repositories.order_repository import OrderRepository
from app.repositories.product_repository import ProductRepository
from app.models.order import OrderCreate
from app.core.exceptions import ValidationError, NotFoundError


class OrderService:
    """Order service class"""
    
    def __init__(self):
        self.order_repository = OrderRepository()
        self.product_repository = ProductRepository()
        self.logger = logging.getLogger(__name__)
    
    async def create_order(self, order_data: OrderCreate) -> Dict[str, str]:
        """Create a new order"""
        # Validate order data
        await self._validate_order_data(order_data)
        
        # Calculate total
        total = await self._calculate_order_total(order_data)
        
        # Create order
        order_id = await self.order_repository.create_order(order_data, total)
        
        return {"id": order_id}
    
    async def get_user_orders(
        self,
        user_id: str,
        limit: int = 10,
        offset: int = 0
    ) -> Dict[str, Any]:
        """Get orders for a specific user"""
        # Validate pagination parameters
        if limit <= 0 or limit > 100:
            raise ValidationError("Limit must be between 1 and 100")
        
        if offset < 0:
            raise ValidationError("Offset must be non-negative")
        
        orders, page_info = await self.order_repository.get_user_orders(
            user_id=user_id,
            limit=limit,
            offset=offset
        )
        
        return {
            "data": orders,
            "page": page_info
        }
    
    async def _validate_order_data(self, order_data: OrderCreate):
        """Validate order data"""
        # Check for duplicate product IDs
        product_ids = [item.productId for item in order_data.items]
        if len(product_ids) != len(set(product_ids)):
            raise ValidationError("Duplicate products in order are not allowed")
        
        # Validate that all products exist
        products = await self.product_repository.get_products_by_ids(product_ids)
        found_product_ids = {product["id"] for product in products}
        
        for product_id in product_ids:
            if product_id not in found_product_ids:
                raise NotFoundError(f"Product with ID {product_id} not found")
    
    async def _calculate_order_total(self, order_data: OrderCreate) -> float:
        """Calculate total order amount"""
        product_ids = [item.productId for item in order_data.items]
        products = await self.product_repository.get_products_by_ids(product_ids)
        
        # Create price lookup map
        price_map = {product["id"]: product["price"] for product in products}
        
        total = 0.0
        for item in order_data.items:
            price = price_map.get(item.productId, 0.0)
            total += price * item.qty
        
        return total
