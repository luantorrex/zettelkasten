from fastapi import APIRouter, HTTPException, status
from typing import List
import logging

from ..models.note import Note, NoteCreate, NoteUpdate
from ..controllers.note_controller import (
    create_note,
    list_notes,
    get_note,
    update_note,
    delete_note,
)

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/", response_model=Note, status_code=status.HTTP_201_CREATED)
async def create(data: NoteCreate):
    logger.info("POST /notes/ with data: %s", data)
    try:
        note = await create_note(data)
        logger.info("Note created with id %s", note.id)
        return note
    except ValueError as e:
        logger.error("Error creating note: %s", e)
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/", response_model=List[Note])
async def index():
    return await list_notes()


@router.get("/{note_id}", response_model=Note)
async def show(note_id: str):
    note = await get_note(note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.put("/{note_id}", response_model=Note)
async def update(note_id: str, data: NoteUpdate):
    try:
        note = await update_note(note_id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def destroy(note_id: str):
    success = await delete_note(note_id)
    if not success:
        raise HTTPException(status_code=404, detail="Note not found")
