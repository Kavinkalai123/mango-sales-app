from bson import ObjectId
from app.schema.order_schema import (
    OrderCreate,
    OrderUpdate,
    OrderResponse,
)
from typing import List


async def get_orders(db, skip: int = 0, limit: int = 100) -> List[OrderResponse]:
    orders = []
    cursor = db.orders.find().skip(skip).limit(limit)
    async for doc in cursor:
        doc["id"] = str(doc.pop("_id"))
        orders.append(OrderResponse(**doc))
    return orders


async def get_order(db, order_id: str) -> OrderResponse:
    from bson.errors import InvalidId
    try:
        doc = await db.orders.find_one({"_id": ObjectId(order_id)})
    except InvalidId:
        return None
    
    if not doc:
        return None
    
    doc["id"] = str(doc.pop("_id"))
    return OrderResponse(**doc)


async def create_order(db, order: OrderCreate) -> OrderResponse:
    from bson.errors import InvalidId
    
    # Calculate total and validate products
    total_amount = 0
    order_items_data = []
    
    for item in order.items:
        try:
            product_id = ObjectId(item.product_id)
        except InvalidId:
            raise ValueError(f"Invalid product ID: {item.product_id}")
        
        product = await db.products.find_one({"_id": product_id})
        if not product:
            raise ValueError(f"Product with id {item.product_id} not found")
        
        subtotal = item.quantity * item.price_per_kg
        total_amount += subtotal
        order_items_data.append({
            "product_id": item.product_id,
            "product_name": product.get("name", ""),
            "quantity": item.quantity,
            "price_per_kg": item.price_per_kg,
            "subtotal": subtotal
        })
        
        # Update stock quantity
        await db.products.update_one(
            {"_id": product_id},
            {"$inc": {"stock_quantity": -item.quantity}}
        )
    
    # Create order
    order_dict = order.model_dump()
    order_dict["total_amount"] = total_amount
    order_dict["status"] = "pending"
    order_dict["items"] = order_items_data
    
    result = await db.orders.insert_one(order_dict)
    order_dict["id"] = str(result.inserted_id)
    return OrderResponse(**order_dict)


async def update_order_status(db, order_id: str, status: str) -> OrderResponse:
    from bson.errors import InvalidId
    try:
        obj_id = ObjectId(order_id)
    except InvalidId:
        return None
    
    await db.orders.update_one({"_id": obj_id}, {"$set": {"status": status}})
    return await get_order(db, order_id)


async def delete_order(db, order_id: str) -> bool:
    from bson.errors import InvalidId
    try:
        obj_id = ObjectId(order_id)
    except InvalidId:
        return False
    
    result = await db.orders.delete_one({"_id": obj_id})
    return result.deleted_count > 0