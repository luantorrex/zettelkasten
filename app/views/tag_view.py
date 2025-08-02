from fastapi import APIRouter, HTTPException, status
from typing import Dict, List
import logging

from ..models.tag import Tag, TagCreate, TagUpdate
from ..controllers.tag_controller import (
    create_tag,
    list_tags,
    get_tag,
    update_tag,
    delete_tag,
)

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/", response_model=Tag, status_code=status.HTTP_201_CREATED)
async def create(data: TagCreate):
    logger.info("POST /tags/ with data: %s", data)
    return await create_tag(data)


@router.get("/", response_model=Dict[str, List[str]])
async def index():
    return await list_tags()


@router.get("/{user_id}", response_model=Dict[str, List[str]])
async def show(user_id: str):
    result = await get_tag(user_id)
    if result is None:
        raise HTTPException(status_code=404, detail="User tags not found")
    return result


@router.put("/{user_id}", response_model=Tag)
async def update(user_id: str, data: TagUpdate):
    result = await update_tag(user_id, data)
    if result is None:
        raise HTTPException(status_code=404, detail="User tags not found")
    return result


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def destroy(user_id: str):
    success = await delete_tag(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User tags not found")
