from bson import ObjectId
import logging
from typing import List

from ..database import db
from ..models.favorite import Favorite, FavoriteCreate
from ..models.note import Note

favorites_collection = db["favorites"]
notes_collection = db["notes"]
users_collection = db["users"]

logger = logging.getLogger(__name__)


async def add_favorite(data: FavoriteCreate) -> Favorite:
    logger.info(
        "Adding favorite for user %s and note %s", data.userId, data.noteId
    )
    if not await users_collection.find_one({"_id": ObjectId(data.userId)}):
        logger.error("User %s not found", data.userId)
        raise ValueError("User not found")
    if not await notes_collection.find_one({"_id": ObjectId(data.noteId)}):
        logger.error("Note %s not found", data.noteId)
        raise ValueError("Note not found")

    user_oid = ObjectId(data.userId)
    note_oid = ObjectId(data.noteId)
    await favorites_collection.update_one(
        {"userId": user_oid},
        {"$addToSet": {"noteIds": note_oid}},
        upsert=True,
    )
    doc = await favorites_collection.find_one({"userId": user_oid}, {"_id": 0})
    return Favorite(**doc)


async def get_favorite_notes(user_id: str) -> List[Note]:
    logger.info("Listing favorite notes for user %s", user_id)
    if not await users_collection.find_one({"_id": ObjectId(user_id)}):
        logger.error("User %s not found", user_id)
        raise ValueError("User not found")

    doc = await favorites_collection.find_one({"userId": ObjectId(user_id)})
    if not doc or not doc.get("noteIds"):
        return []

    note_ids = doc["noteIds"]
    notes_cursor = notes_collection.find({"_id": {"$in": note_ids}})
    notes: List[Note] = []
    async for doc in notes_cursor:
        notes.append(Note(**doc))
    return notes


async def delete_favorite(note_id: str) -> bool:
    result = await favorites_collection.update_one(
        {"noteIds": ObjectId(note_id)},
        {"$pull": {"noteIds": ObjectId(note_id)}},
    )
    return result.modified_count == 1
