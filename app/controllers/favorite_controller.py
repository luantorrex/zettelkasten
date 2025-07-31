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

    favorite_data = data.model_dump(by_alias=True)
    favorite_data["userId"] = ObjectId(favorite_data["userId"])
    favorite_data["noteId"] = ObjectId(favorite_data["noteId"])
    result = await favorites_collection.insert_one(favorite_data)
    logger.info("Favorite inserted with id %s", result.inserted_id)
    doc = await favorites_collection.find_one({"_id": result.inserted_id})
    return Favorite(**doc)


async def get_favorite_notes(user_id: str) -> List[Note]:
    logger.info("Listing favorite notes for user %s", user_id)
    if not await users_collection.find_one({"_id": ObjectId(user_id)}):
        logger.error("User %s not found", user_id)
        raise ValueError("User not found")

    favorites_cursor = favorites_collection.find({"userId": ObjectId(user_id)})
    note_ids = [fav["noteId"] async for fav in favorites_cursor]
    if not note_ids:
        return []

    notes_cursor = notes_collection.find({"_id": {"$in": note_ids}})
    notes: List[Note] = []
    async for doc in notes_cursor:
        notes.append(Note(**doc))
    return notes


async def delete_favorite(note_id: str) -> bool:
    result = await favorites_collection.delete_one({"noteId": ObjectId(note_id)})
    return result.deleted_count == 1
