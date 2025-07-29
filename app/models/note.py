from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class NoteBase(BaseModel):
    title: str
    content: str


class NoteCreate(NoteBase):
    pass


class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class Note(NoteBase):
    id: str = Field(alias="_id")

    model_config = ConfigDict(populate_by_name=True)
