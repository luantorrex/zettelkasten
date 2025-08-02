from pydantic import BaseModel
from typing import Optional


class TagBase(BaseModel):
    title: str
    description: str
    parent_note_id: str


class TagCreate(TagBase):
    userId: str


class TagUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    parent_note_id: Optional[str] = None


class Tag(TagCreate):
    tag_id: str
