from pydantic import BaseModel, Field
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

    class Config:
        allow_population_by_field_name = True
