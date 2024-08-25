from fastapi import APIRouter, HTTPException, Depends
from models.user import User
from typing import List
from bson import ObjectId
from pydantic import BaseModel, EmailStr

router = APIRouter()

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    password: str

class UserUpdate(BaseModel):
    email: EmailStr = None
    username: str = None
    first_name: str = None
    last_name: str = None

class UserResponse(BaseModel):
    user_id: str
    email: EmailStr
    username: str
    first_name: str
    last_name: str

@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate):
    existing_user = User.objects(email=user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(
        email=user.email,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name
    )
    new_user.set_password(user.password)
    new_user.save()
    return UserResponse(
        user_id=str(new_user.user_id),
        email=new_user.email,
        username=new_user.username,
        first_name=new_user.first_name,
        last_name=new_user.last_name
    )

@router.get("/{user_id}", response_model=UserResponse)
async def read_user(user_id: str):
    user = User.objects(user_id=user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(
        user_id=str(user.user_id),
        email=user.email,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name
    )

@router.get("/", response_model=List[UserResponse])
async def read_users():
    users = User.objects()
    return [
        UserResponse(
            user_id=str(user.user_id),
            email=user.email,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name
        ) for user in users
    ]

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, user: UserUpdate):
    db_user = User.objects(user_id=user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = user.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    db_user.save()
    return UserResponse(
        user_id=str(db_user.user_id),
        email=db_user.email,
        username=db_user.username,
        first_name=db_user.first_name,
        last_name=db_user.last_name
    )

@router.delete("/{user_id}", response_model=dict)
async def delete_user(user_id: str):
    user = User.objects(user_id=user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user.delete()
    return {"message": "User deleted successfully"}
