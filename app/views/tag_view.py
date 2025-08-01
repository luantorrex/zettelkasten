from fastapi import APIRouter, HTTPException, status
from typing import List
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


@router.get("/", response_model=List[Tag])
async def index():
    return await list_tags()


@router.get("/{tag}", response_model=Tag)
async def show(tag: str):
    result = await get_tag(tag)
    if result is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return result


@router.put("/{tag}", response_model=Tag)
async def update(tag: str, data: TagUpdate):
    result = await update_tag(tag, data)
    if result is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return result


@router.delete("/{tag}", status_code=status.HTTP_204_NO_CONTENT)
async def destroy(tag: str):
    success = await delete_tag(tag)
    if not success:
        raise HTTPException(status_code=404, detail="Tag not found")
