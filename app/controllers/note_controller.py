from bson import ObjectId
from typing import List, Optional
import logging

from ..database import db
from ..models.note import Note, NoteCreate, NoteUpdate

collection = db["notes"]
users_collection = db["users"]

logger = logging.getLogger(__name__)


async def create_note(data: NoteCreate) -> Note:
    logger.info("Creating note for user %s with title '%s'", data.userId, data.title)
    if not await users_collection.find_one({"_id": ObjectId(data.userId)}):
        logger.error("User %s not found", data.userId)
        raise ValueError("User not found")

    note_data = data.model_dump(by_alias=True)
    note_data["userId"] = ObjectId(note_data["userId"])
    result = await collection.insert_one(note_data)
    logger.info("Note inserted with id %s", result.inserted_id)
    doc = await collection.find_one({"_id": result.inserted_id})
    return Note(**doc)


async def list_notes() -> List[Note]:
    notes = []
    async for doc in collection.find():
        notes.append(Note(**doc))
    return notes


async def list_notes_by_user(user_id: str) -> List[Note]:
    logger.info("Listing notes for user %s", user_id)
    if not await users_collection.find_one({"_id": ObjectId(user_id)}):
        logger.error("User %s not found", user_id)
        raise ValueError("User not found")

    notes: List[Note] = []
    cursor = collection.find({"userId": ObjectId(user_id)})
    async for doc in cursor:
        notes.append(Note(**doc))
    return notes


async def get_note(note_id: str) -> Optional[Note]:
    doc = await collection.find_one({"_id": ObjectId(note_id)})
    return Note(**doc) if doc else None


async def update_note(note_id: str, data: NoteUpdate) -> Optional[Note]:
    update_data = data.model_dump(exclude_unset=True, by_alias=True)
    if "userId" in update_data:
        if not await users_collection.find_one({"_id": ObjectId(update_data["userId"])}):
            raise ValueError("User not found")
        update_data["userId"] = ObjectId(update_data["userId"])

    await collection.update_one({"_id": ObjectId(note_id)}, {"$set": update_data})
    return await get_note(note_id)


async def delete_note(note_id: str) -> bool:
    result = await collection.delete_one({"_id": ObjectId(note_id)})
    return result.deleted_count == 1
