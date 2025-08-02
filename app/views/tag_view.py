from fastapi import APIRouter, HTTPException, status
from typing import List
import logging

from ..models.tag import Tag, TagCreate, TagUpdate
from ..controllers.tag_controller import (
    create_tag,
    list_tags,
    list_user_tags,
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


@router.get("/", response_model=List[Tag])
async def index():
    return await list_tags()


@router.get("/user/{user_id}", response_model=List[Tag])
async def user_tags(user_id: str):
    return await list_user_tags(user_id)


@router.get("/{tag_id}", response_model=Tag)
async def show(tag_id: str):
    result = await get_tag(tag_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return result


@router.put("/{tag_id}", response_model=Tag)
async def update(tag_id: str, data: TagUpdate):
    result = await update_tag(tag_id, data)
    if result is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return result


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
async def destroy(tag_id: str):
    success = await delete_tag(tag_id)
    if not success:
        raise HTTPException(status_code=404, detail="Tag not found")
