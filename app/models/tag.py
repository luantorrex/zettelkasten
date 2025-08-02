from pydantic import BaseModel
from typing import List


class TagBase(BaseModel):
    tags: List[str]


class TagCreate(TagBase):
    userId: str


class TagUpdate(BaseModel):
    tags: List[str]


class Tag(TagCreate):
    pass
