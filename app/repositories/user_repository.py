"""User repository"""
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, user: User) -> User:
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
    
    async def get_by_id(self, user_id: int) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
    
    async def get_by_username(self, username: str) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()
    
    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        query = select(User).offset(skip).limit(limit).order_by(User.created_at.desc())
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def update(self, user: User) -> User:
        await self.db.commit()
        await self.db.refresh(user)
        return user
    
    async def delete(self, user_id: int) -> bool:
        user = await self.get_by_id(user_id)
        if user:
            await self.db.delete(user)
            await self.db.commit()
            return True
        return False
