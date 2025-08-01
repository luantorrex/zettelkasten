from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import List


class FavoriteCreate(BaseModel):
    userId: str
    noteId: str


class Favorite(BaseModel):
    userId: str
    noteIds: List[str] = Field(default_factory=list)

    model_config = ConfigDict(populate_by_name=True)

    @field_validator("userId", mode="before")
    def convert_user_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

    @field_validator("noteIds", mode="before")
    def convert_note_ids(cls, v):
        if isinstance(v, list):
            return [str(i) if isinstance(i, ObjectId) else i for i in v]
        return v
