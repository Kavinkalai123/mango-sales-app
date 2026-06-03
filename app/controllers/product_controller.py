from bson import ObjectId
from app.schema.product_schema import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
)
from typing import List


async def get_products(db, skip: int = 0, limit: int = 100) -> List[ProductResponse]:
    products = []
    cursor = db.products.find().skip(skip).limit(limit)
    async for doc in cursor:
        doc["id"] = str(doc.pop("_id"))
        products.append(ProductResponse(**doc))
    return products


async def get_product(db, product_id: str) -> ProductResponse:
    from bson.errors import InvalidId
    try:
        doc = await db.products.find_one({"_id": ObjectId(product_id)})
    except InvalidId:
        return None
    
    if not doc:
        return None
    
    doc["id"] = str(doc.pop("_id"))
    return ProductResponse(**doc)


async def create_product(db, product: ProductCreate) -> ProductResponse:
    product_dict = product.model_dump()
    result = await db.products.insert_one(product_dict)
    product_dict["id"] = str(result.inserted_id)
    return ProductResponse(**product_dict)


async def update_product(db, product_id: str, product: ProductUpdate) -> ProductResponse:
    from bson.errors import InvalidId
    try:
        obj_id = ObjectId(product_id)
    except InvalidId:
        return None
    
    update_data = product.model_dump(exclude_unset=True)
    if not update_data:
        return await get_product(db, product_id)
    
    await db.products.update_one({"_id": obj_id}, {"$set": update_data})
    return await get_product(db, product_id)


async def delete_product(db, product_id: str) -> bool:
    from bson.errors import InvalidId
    try:
        obj_id = ObjectId(product_id)
    except InvalidId:
        return False
    
    result = await db.products.delete_one({"_id": obj_id})
    return result.deleted_count > 0


async def update_product_image(db, product_id: str, image_url: str):
    from bson.errors import InvalidId
    try:
        obj_id = ObjectId(product_id)
    except InvalidId:
        return None

    await db.products.update_one({"_id": obj_id}, {"$set": {"image_url": image_url}})
    return await get_product(db, product_id)