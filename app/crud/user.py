from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.type import RoleType
from app.core.security_utils import hash_password
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate



async def create_user(db: AsyncSession, user: UserCreate) -> User:
    password_hash = hash_password(user.password)
    new_user = User(**user.model_dump(exclude={'password'}), password_hash=password_hash, role=RoleType.USER)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def get_user_by_id(user_id: int, db: AsyncSession) -> User | None:
    user = await db.get(User, user_id)
    return user


async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().one_or_none()
    return user


async def get_user_by_email(db:AsyncSession, email: EmailStr) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalars().one_or_none()
    return user


async def update_user(db: AsyncSession, user: User, updates: UserUpdate) -> User | None:
    if not user:
        return None
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    await db.commit()
    await db.refresh(user)
    return user


async def delete_user(db: AsyncSession, user_id: int):
    user = await db.get(User, user_id)
    if not user:
        return None
    db.delete(user)
    await db.commit()
    return True


