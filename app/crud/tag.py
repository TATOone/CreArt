from sqlalchemy.orm import Session
from app.models.tag import Tag
from app.schemas.tag import TagCreate


def create_tag(db: Session, tag: TagCreate):
    new_tag = Tag(**tag.model_dump())
    db.add(new_tag)
    db.commit()
    db.refresh(new_tag)
    return new_tag

def get_tag(db: Session, tag_id: int):
    return db.query(Tag).filter(Tag.id == tag_id).first()

def get_tag_by_name(db: Session, tag_name: str):
    return db.query(Tag).filter(Tag.name == tag_name).first()