from bson import ObjectId
from pydantic import BaseModel, Field, ConfigDict, EmailStr, field_validator
from typing import Optional


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class User(UserBase):
    id: str = Field(alias="_id")
    password: str

    model_config = ConfigDict(populate_by_name=True)

    @field_validator("id", mode="before")
    def convert_object_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v
