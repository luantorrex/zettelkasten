from bson import ObjectId
from typing import List, Optional

from ..database import db
from ..models.note import Note, NoteCreate, NoteUpdate

collection = db["notes"]


async def create_note(data: NoteCreate) -> Note:
    result = await collection.insert_one(data.model_dump())
    doc = await collection.find_one({"_id": result.inserted_id})
    return Note(**doc)


async def list_notes() -> List[Note]:
    notes = []
    async for doc in collection.find():
        notes.append(Note(**doc))
    return notes


async def get_note(note_id: str) -> Optional[Note]:
    doc = await collection.find_one({"_id": ObjectId(note_id)})
    return Note(**doc) if doc else None


async def update_note(note_id: str, data: NoteUpdate) -> Optional[Note]:
    await collection.update_one(
        {"_id": ObjectId(note_id)}, {"$set": data.model_dump(exclude_unset=True)}
    )
    return await get_note(note_id)


async def delete_note(note_id: str) -> bool:
    result = await collection.delete_one({"_id": ObjectId(note_id)})
    return result.deleted_count == 1
