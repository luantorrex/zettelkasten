from fastapi import APIRouter, HTTPException, status
from typing import List

from ..models.user import User, UserCreate, UserLogin, UserUpdate
from ..controllers.user_controller import (
    create_user,
    list_users,
    get_user,
    update_user,
    delete_user,
    find_user_by_credentials,
)

router = APIRouter()


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create(data: UserCreate):
    return await create_user(data)


@router.get("/", response_model=List[User])
async def index():
    return await list_users()


@router.get("/{userId}", response_model=User)
async def show(userId: str):
    user = await get_user(userId)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{userId}", response_model=User)
async def update(userId: str, data: UserUpdate):
    user = await update_user(userId, data)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{userId}", status_code=status.HTTP_204_NO_CONTENT)
async def destroy(userId: str):
    success = await delete_user(userId)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")


@router.post("/verify", response_model=User)
async def verify(data: UserLogin):
    user = await find_user_by_credentials(data.username, data.password)
    if user is None:
        raise HTTPException(status_code=400, detail="User not found")
    return user
