"""
Script to seed the database with sample data
"""
import asyncio
import logging
from motor.motor_asyncio import AsyncIOMotorClient

# Sample data
SAMPLE_PRODUCTS = [
    {
        "name": "Classic T-Shirt",
        "price": 29.99,
        "sizes": [
            {"size": "small", "quantity": 50},
            {"size": "medium", "quantity": 75},
            {"size": "large", "quantity": 40},
            {"size": "xl", "quantity": 25}
        ]
    },
    {
        "name": "Denim Jeans",
        "price": 79.99,
        "sizes": [
            {"size": "28", "quantity": 20},
            {"size": "30", "quantity": 35},
            {"size": "32", "quantity": 45},
            {"size": "34", "quantity": 30},
            {"size": "36", "quantity": 15}
        ]
    },
    {
        "name": "Running Shoes",
        "price": 129.99,
        "sizes": [
            {"size": "8", "quantity": 25},
            {"size": "9", "quantity": 40},
            {"size": "10", "quantity": 35},
            {"size": "11", "quantity": 20},
            {"size": "12", "quantity": 10}
        ]
    },
    {
        "name": "Winter Jacket",
        "price": 199.99,
        "sizes": [
            {"size": "small", "quantity": 15},
            {"size": "medium", "quantity": 25},
            {"size": "large", "quantity": 20},
            {"size": "xl", "quantity": 10}
        ]
    },
    {
        "name": "Baseball Cap",
        "price": 24.99,
        "sizes": [
            {"size": "one-size", "quantity": 100}
        ]
    }
]


async def seed_database():
    """Seed the database with sample data"""
    try:
        # Connect to MongoDB
        client = AsyncIOMotorClient("mongodb://localhost:27017")
        db = client.ecommerce_db
        
        # Clear existing data
        await db.products.delete_many({})
        await db.orders.delete_many({})
        
        # Insert sample products
        result = await db.products.insert_many(SAMPLE_PRODUCTS)
        print(f"Inserted {len(result.inserted_ids)} products")
        
        # Create indexes
        await db.products.create_index("name")
        await db.products.create_index("sizes.size")
        await db.orders.create_index("userId")
        await db.orders.create_index("createdAt")
        
        print("Database seeded successfully!")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
    finally:
        client.close()


if __name__ == "__main__":
    asyncio.run(seed_database())
