from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Optional
import os
from app.config.logger import get_logger

logger = get_logger()

# MongoDB connection settings
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "mango_ecommerce")

# Global motor client and database
client: Optional[AsyncIOMotorClient] = None
db: Optional[AsyncIOMotorDatabase] = None


async def connect_to_mongodb():
    """Connect to MongoDB"""
    global client, db
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[MONGODB_DB_NAME]
    # Create indexes
    await create_indexes()
    logger.info(f"Connected to MongoDB: {MONGODB_DB_NAME}")


async def close_mongodb_connection():
    """Close MongoDB connection"""
    global client
    if client:
        client.close()
        logger.info("MongoDB connection closed")


def get_database() -> AsyncIOMotorDatabase:
    """Get database instance"""
    if db is None:
        raise RuntimeError("Database connection has not been initialized")
    return db


async def create_indexes():
    """Create database indexes"""
    # Products indexes
    await db.products.create_index("name")
    await db.products.create_index("variety")
    await db.products.create_index([("name", 2), ("variety", 1)])
    
    # Users indexes
    await db.users.create_index("email", unique=True)
    await db.users.create_index("phone")
    
    # Orders indexes
    await db.orders.create_index("user_id")
    await db.orders.create_index("status")
    await db.orders.create_index("created_at")
    await db.order_items.create_index("order_id")
    await db.order_items.create_index("product_id")