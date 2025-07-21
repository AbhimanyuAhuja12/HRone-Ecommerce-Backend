"""
Order repository for database operations
"""
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from bson import ObjectId
from pymongo.errors import PyMongoError

from app.core.database import get_database
from app.core.exceptions import DatabaseError
from app.models.order import OrderCreate


class OrderRepository:
    """Order repository class"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    async def create_order(self, order_data: OrderCreate, total: float) -> str:
        """Create a new order"""
        try:
            db = await get_database()
            
            order_dict = {
                "userId": order_data.userId,
                "items": [item.dict() for item in order_data.items],
                "total": total,
                "createdAt": datetime.utcnow()
            }
            
            result = await db.orders.insert_one(order_dict)
            
            self.logger.info(f"Order created with ID: {result.inserted_id}")
            return str(result.inserted_id)
            
        except PyMongoError as e:
            self.logger.error(f"Failed to create order: {e}")
            raise DatabaseError("Failed to create order")
    
    async def get_user_orders(
        self,
        user_id: str,
        limit: int = 10,
        offset: int = 0
    ) -> tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """Get orders for a specific user with pagination"""
        try:
            db = await get_database()
            
            # Build aggregation pipeline
            pipeline = [
                {"$match": {"userId": user_id}},
                {"$sort": {"_id": 1}},
                {"$skip": offset},
                {"$limit": limit},
                {
                    "$lookup": {
                        "from": "products",
                        "let": {"item_ids": "$items.productId"},
                        "pipeline": [
                            {
                                "$match": {
                                    "$expr": {
                                        "$in": [{"$toString": "$_id"}, "$$item_ids"]
                                    }
                                }
                            },
                            {
                                "$project": {
                                    "_id": 1,
                                    "name": 1,
                                    "price": 1
                                }
                            }
                        ],
                        "as": "productDetails"
                    }
                }
            ]
            
            # Execute aggregation
            cursor = db.orders.aggregate(pipeline)
            orders = await cursor.to_list(length=limit)
            
            # Get total count for pagination
            total_count = await db.orders.count_documents({"userId": user_id})
            
            # Format response
            formatted_orders = []
            for order in orders:
                # Create product lookup map
                product_map = {}
                for product in order.get("productDetails", []):
                    product_map[str(product["_id"])] = {
                        "id": str(product["_id"]),
                        "name": product["name"]
                    }
                
                # Format order items with product details
                formatted_items = []
                for item in order["items"]:
                    product_details = product_map.get(item["productId"], {
                        "id": item["productId"],
                        "name": "Unknown Product"
                    })
                    
                    formatted_items.append({
                        "productDetails": product_details,
                        "qty": item["qty"]
                    })
                
                formatted_orders.append({
                    "id": str(order["_id"]),
                    "items": formatted_items,
                    "total": order["total"]
                })
            
            # Calculate pagination info
            next_offset = offset + limit if offset + limit < total_count else None
            previous_offset = max(0, offset - limit) if offset > 0 else None
            
            page_info = {
                "next": str(next_offset) if next_offset is not None else None,
                "limit": len(formatted_orders),
                "previous": str(previous_offset) if previous_offset is not None else None
            }
            
            self.logger.info(f"Retrieved {len(formatted_orders)} orders for user {user_id}")
            return formatted_orders, page_info
            
        except PyMongoError as e:
            self.logger.error(f"Failed to get user orders: {e}")
            raise DatabaseError("Failed to retrieve orders")
