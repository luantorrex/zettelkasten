from bson import ObjectId
from typing import List, Optional

from ..database import db
from ..models.user import User, UserCreate, UserUpdate

collection = db["users"]


async def create_user(data: UserCreate) -> User:
    result = await collection.insert_one(data.model_dump())
    doc = await collection.find_one({"_id": result.inserted_id})
    return User(**doc)


async def list_users() -> List[User]:
    users: List[User] = []
    async for doc in collection.find():
        users.append(User(**doc))
    return users


async def get_user(user_id: str) -> Optional[User]:
    doc = await collection.find_one({"_id": ObjectId(user_id)})
    return User(**doc) if doc else None


async def update_user(user_id: str, data: UserUpdate) -> Optional[User]:
    await collection.update_one(
        {"_id": ObjectId(user_id)}, {"$set": data.model_dump(exclude_unset=True)}
    )
    return await get_user(user_id)


async def delete_user(user_id: str) -> bool:
    result = await collection.delete_one({"_id": ObjectId(user_id)})
    return result.deleted_count == 1
