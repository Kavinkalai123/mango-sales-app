from bson import ObjectId
from app.schema.user_schema import (
    UserCreate,
    UserUpdate,
    UserResponse,
)
from app.utils.auth import get_password_hash, verify_password
from typing import List


async def get_users(db, skip: int = 0, limit: int = 100) -> List[UserResponse]:
    users = []
    cursor = db.users.find().skip(skip).limit(limit)
    async for doc in cursor:
        doc["id"] = str(doc.pop("_id"))
        users.append(UserResponse(**doc))
    return users


async def get_user(db, user_id: str) -> UserResponse:
    from bson.errors import InvalidId
    try:
        doc = await db.users.find_one({"_id": ObjectId(user_id)})
    except InvalidId:
        return None
    
    if not doc:
        return None
    
    doc["id"] = str(doc.pop("_id"))
    return UserResponse(**doc)


async def get_user_by_email(db, email: str) -> UserResponse:
    doc = await db.users.find_one({"email": email})
    if not doc:
        return None
    
    doc["id"] = str(doc.pop("_id"))
    return UserResponse(**doc)


async def create_user(db, user: UserCreate) -> UserResponse:
    user_dict = user.model_dump()
    user_dict["password"] = get_password_hash(user_dict["password"])
    result = await db.users.insert_one(user_dict)
    user_dict["id"] = str(result.inserted_id)
    user_dict.pop("password", None)
    return UserResponse(**user_dict)


async def authenticate_user(db, email: str, password: str) -> UserResponse:
    doc = await db.users.find_one({"email": email})
    if not doc:
        return None

    if not verify_password(password, doc.get("password", "")):
        return None

    doc.pop("password", None)
    doc["id"] = str(doc.pop("_id"))
    return UserResponse(**doc)


async def update_user(db, user_id: str, user: UserUpdate) -> UserResponse:
    from bson.errors import InvalidId
    try:
        obj_id = ObjectId(user_id)
    except InvalidId:
        return None
    
    update_data = user.model_dump(exclude_unset=True)
    if not update_data:
        return await get_user(db, user_id)
    
    await db.users.update_one({"_id": obj_id}, {"$set": update_data})
    return await get_user(db, user_id)


async def delete_user(db, user_id: str) -> bool:
    from bson.errors import InvalidId
    try:
        obj_id = ObjectId(user_id)
    except InvalidId:
        return False
    
    result = await db.users.delete_one({"_id": obj_id})
    return result.deleted_count > 0