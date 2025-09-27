from datetime import timedelta, datetime, timezone


import bcrypt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status

from app.core.database import SessionLocal
from app.crud.tag import get_tag_by_name
from app.crud.user import get_user_by_id
from app.models.tag import Tag
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_db():
    session: Session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_current_user(token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Неверный токен",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
            raise credentials_exception

    user = get_user_by_id(db, user_id)
    if user is None:
        raise credentials_exception
    return user


def resolved_tags(db: Session, tags: list) -> list:
    """ При создании поста с тегами, добавляет новые теги в БД и возвращает список тегов, которые знакомы базе данных """
    resolved = []
    for tag_schema in tags:
        tag = get_tag_by_name(db, tag_schema.name)
        if not tag:
            tag = Tag(name=tag_schema.name)
            db.add(tag)
        resolved.append(tag)
    return resolved


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({'exp': expire})
    token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token
