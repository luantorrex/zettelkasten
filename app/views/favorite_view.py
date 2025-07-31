from fastapi import APIRouter, HTTPException, status
from typing import List
import logging

from ..models.favorite import Favorite, FavoriteCreate
from ..models.note import Note
from ..controllers.favorite_controller import (
    add_favorite,
    delete_favorite,
    get_favorite_notes,
)

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/", response_model=Favorite, status_code=status.HTTP_201_CREATED)
async def create(data: FavoriteCreate):
    logger.info("POST /favorites/ with data: %s", data)
    try:
        favorite = await add_favorite(data)
        logger.info("Favorite created with id %s", favorite.id)
        return favorite
    except ValueError as e:
        logger.error("Error creating favorite: %s", e)
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{user_id}", response_model=List[Note])
async def index(user_id: str):
    logger.info("GET /favorites/%s", user_id)
    try:
        return await get_favorite_notes(user_id)
    except ValueError as e:
        logger.error("Error listing favorites for user %s: %s", user_id, e)
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def destroy(note_id: str):
    success = await delete_favorite(note_id)
    if not success:
        raise HTTPException(status_code=404, detail="Favorite not found")
