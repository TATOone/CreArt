from sqlalchemy.orm import Session

from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentUpdate


def create_comment(db: Session, comment: CommentCreate) -> Comment:
    new_comment = Comment(**comment.model_dump())
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


def get_comment_by_id(db: Session, comment_id: int) -> Comment | None:
    return db.query(Comment).filter(Comment.id == comment_id).first()


def get_comments_by_post(db: Session, post_id: int) -> list[Comment]:
    return db.query(Comment).filter(Comment.post_id == post_id).all()


def update_comment(db: Session, comment_id: int, updates: CommentUpdate) -> Comment:
    comment = get_comment_by_id(db, comment_id)
    if not comment:
        return None
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(comment, field, value)
    db.commit()
    db.refresh(comment)
    return comment

def delete_comment(db: Session, comment_id: int):
    comment = get_comment_by_id(db, comment_id)
    if not comment:
        return None
    db.delete(comment)
    db.commit()
    return True
