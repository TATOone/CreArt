from sqlalchemy.orm import Session

from app.crud.tag import get_tag_by_name
from app.models.post import Post
from app.models.tag import Tag


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
