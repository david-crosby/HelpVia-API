"""Authentication API"""
import logging
from typing import Annotated
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.auth import get_current_active_user
from app.core.config import settings
from app.core.database import get_db
from app.core.security import verify_password, get_password_hash, create_access_token
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserResponse, Token

logger = logging.getLogger("helpvia")
router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    logger.info(f"Registering user: {user_data.username}")
    user_repo = UserRepository(db)
    if await user_repo.get_by_username(user_data.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    if await user_repo.get_by_email(user_data.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(username=user_data.username, email=user_data.email, full_name=user_data.full_name, hashed_password=get_password_hash(user_data.password))
    return await user_repo.create(user)

@router.post("/login", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: AsyncSession = Depends(get_db)):
    user_repo = UserRepository(db)
    user = await user_repo.get_by_username(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    return Token(access_token=token)

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user
