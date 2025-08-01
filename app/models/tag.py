from pydantic import BaseModel
from typing import Optional


class TagBase(BaseModel):
    description: Optional[str] = None


class TagCreate(TagBase):
    tag: str


class TagUpdate(BaseModel):
    description: Optional[str] = None


class Tag(TagCreate):
    pass
