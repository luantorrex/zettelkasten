from fastapi import APIRouter, HTTPException, status
from typing import List

from ..models.user import User, UserCreate, UserUpdate
from ..controllers.user_controller import (
    create_user,
    list_users,
    get_user,
    update_user,
    delete_user,
)

router = APIRouter()


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create(data: UserCreate):
    return await create_user(data)


@router.get("/", response_model=List[User])
async def index():
    return await list_users()


@router.get("/{user_id}", response_model=User)
async def show(user_id: str):
    user = await get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=User)
async def update(user_id: str, data: UserUpdate):
    user = await update_user(user_id, data)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def destroy(user_id: str):
    success = await delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
