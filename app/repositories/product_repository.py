"""
Product repository for database operations
"""
import logging
from typing import List, Optional, Dict, Any
from bson import ObjectId
from pymongo.errors import PyMongoError

from app.core.database import get_database
from app.core.exceptions import DatabaseError, NotFoundError
from app.models.product import ProductCreate, ProductInDB


class ProductRepository:
    """Product repository class"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    async def create_product(self, product_data: ProductCreate) -> str:
        """Create a new product"""
        try:
            db = await get_database()
            
            product_dict = product_data.dict()
            result = await db.products.insert_one(product_dict)
            
            self.logger.info(f"Product created with ID: {result.inserted_id}")
            return str(result.inserted_id)
            
        except PyMongoError as e:
            self.logger.error(f"Failed to create product: {e}")
            raise DatabaseError("Failed to create product")
    
    async def get_products(
        self,
        name: Optional[str] = None,
        size: Optional[str] = None,
        limit: int = 10,
        offset: int = 0
    ) -> tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """Get products with filtering and pagination"""
        try:
            db = await get_database()
            
            # Build query filter
            query_filter = {}
            
            if name:
                query_filter["name"] = {"$regex": name, "$options": "i"}
            
            if size:
                query_filter["sizes.size"] = size
            
            # Get total count for pagination
            total_count = await db.products.count_documents(query_filter)
            
            # Execute query with pagination
            cursor = db.products.find(query_filter).skip(offset).limit(limit)
            products = await cursor.to_list(length=limit)
            
            # Convert ObjectId to string and format response
            formatted_products = []
            for product in products:
                formatted_products.append({
                    "id": str(product["_id"]),
                    "name": product["name"],
                    "price": product["price"]
                })
            
            # Calculate pagination info
            next_offset = offset + limit if offset + limit < total_count else None
            previous_offset = max(0, offset - limit) if offset > 0 else None
            
            page_info = {
                "next": str(next_offset) if next_offset is not None else None,
                "limit": len(formatted_products),
                "previous": str(previous_offset) if previous_offset is not None else None
            }
            
            self.logger.info(f"Retrieved {len(formatted_products)} products")
            return formatted_products, page_info
            
        except PyMongoError as e:
            self.logger.error(f"Failed to get products: {e}")
            raise DatabaseError("Failed to retrieve products")
    
    async def get_product_by_id(self, product_id: str) -> Optional[Dict[str, Any]]:
        """Get product by ID"""
        try:
            if not ObjectId.is_valid(product_id):
                return None
                
            db = await get_database()
            product = await db.products.find_one({"_id": ObjectId(product_id)})
            
            if product:
                product["id"] = str(product["_id"])
                del product["_id"]
            
            return product
            
        except PyMongoError as e:
            self.logger.error(f"Failed to get product by ID: {e}")
            raise DatabaseError("Failed to retrieve product")
    
    async def get_products_by_ids(self, product_ids: List[str]) -> List[Dict[str, Any]]:
        """Get multiple products by IDs"""
        try:
            db = await get_database()
            
            # Convert string IDs to ObjectIds
            object_ids = []
            for pid in product_ids:
                if ObjectId.is_valid(pid):
                    object_ids.append(ObjectId(pid))
            
            cursor = db.products.find({"_id": {"$in": object_ids}})
            products = await cursor.to_list(length=None)
            
            # Format response
            formatted_products = []
            for product in products:
                formatted_products.append({
                    "id": str(product["_id"]),
                    "name": product["name"],
                    "price": product["price"],
                    "sizes": product["sizes"]
                })
            
            return formatted_products
            
        except PyMongoError as e:
            self.logger.error(f"Failed to get products by IDs: {e}")
            raise DatabaseError("Failed to retrieve products")
