"""
Product business logic service
"""
import logging
from typing import List, Dict, Any, Optional

from app.repositories.product_repository import ProductRepository
from app.models.product import ProductCreate
from app.core.exceptions import ValidationError


class ProductService:
    """Product service class"""
    
    def __init__(self):
        self.repository = ProductRepository()
        self.logger = logging.getLogger(__name__)
    
    async def create_product(self, product_data: ProductCreate) -> Dict[str, str]:
        """Create a new product"""
        # Validate product data
        await self._validate_product_data(product_data)
        
        # Create product
        product_id = await self.repository.create_product(product_data)
        
        return {"id": product_id}
    
    async def get_products(
        self,
        name: Optional[str] = None,
        size: Optional[str] = None,
        limit: int = 10,
        offset: int = 0
    ) -> Dict[str, Any]:
        """Get products with filtering and pagination"""
        # Validate pagination parameters
        if limit <= 0 or limit > 100:
            raise ValidationError("Limit must be between 1 and 100")
        
        if offset < 0:
            raise ValidationError("Offset must be non-negative")
        
        products, page_info = await self.repository.get_products(
            name=name,
            size=size,
            limit=limit,
            offset=offset
        )
        
        return {
            "data": products,
            "page": page_info
        }
    
    async def _validate_product_data(self, product_data: ProductCreate):
        """Validate product data"""
        # Check for duplicate sizes
        sizes = [size.size for size in product_data.sizes]
        if len(sizes) != len(set(sizes)):
            raise ValidationError("Duplicate sizes are not allowed")
        
        # Validate size names
        for size in product_data.sizes:
            if not size.size.strip():
                raise ValidationError("Size name cannot be empty")
