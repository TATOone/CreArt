from datetime import timedelta, datetime, timezone

import bcrypt
from jose import jwt
from sqlalchemy.orm import Session

from app.crud.tag import get_tag_by_name
from app.models.tag import Tag
from app.core.config import settings


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
