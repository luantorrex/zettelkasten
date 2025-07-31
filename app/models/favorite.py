from bson import ObjectId
from pydantic import BaseModel, Field, ConfigDict, field_validator


class FavoriteBase(BaseModel):
    userId: str
    noteId: str


class FavoriteCreate(FavoriteBase):
    pass


class Favorite(FavoriteBase):
    id: str = Field(alias="_id")

    model_config = ConfigDict(populate_by_name=True)

    @field_validator("id", mode="before")
    def convert_object_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

    @field_validator("userId", "noteId", mode="before")
    def convert_ids(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v
