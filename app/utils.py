from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import SessionLocal
from app.crud.tag import get_tag_by_name
from app.crud.user import get_user_by_id
from app.models.tag import Tag
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.models.type import RoleType

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

async def get_db():
    """ Асинхронное подключение к сессии """
    async with SessionLocal() as session:
        yield session


async def get_current_user(access_token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Неверный токен",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = int(payload.get("sub"))
        if user_id is None:
            raise credentials_exception
    except JWTError:
            raise credentials_exception

    user = await get_user_by_id(db, user_id)
    if user is None:
        raise credentials_exception
    return user


async def resolved_tags(db: AsyncSession, tags: list) -> list:
    """ При создании поста с тегами, добавляет новые теги в БД и возвращает список тегов, которые знакомы базе данных """
    resolved = []
    for tag_schema in tags:
        tag = await get_tag_by_name(db, tag_schema.name)
        if not tag:
            tag = Tag(name=tag_schema.name)
            db.add(tag)
            await db.flush()
        resolved.append(tag)
    return resolved


async def require_admin(access_token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    role_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='Нет прав доступа',
    )

    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Неверный токен",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = int(payload.get('sub'))
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await get_user_by_id(db, user_id)
    if not user:
        raise credentials_exception
    if user.role != RoleType.ADMIN:
        raise role_exception
    return user




