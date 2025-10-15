from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentUpdate


async def create_comment(db: AsyncSession, comment: CommentCreate) -> Comment:
    new_comment = Comment(**comment.model_dump())
    db.add(new_comment)
    await db.commit()
    await db.refresh(new_comment)
    return new_comment


async def get_comment_by_id(db: AsyncSession, comment_id: int) -> Comment | None:
    comment = await db.get(Comment, comment_id)
    return comment


async def get_comments_by_post(db: AsyncSession, post_id: int) -> list[Comment]:
    result = await db.execute(select(Comment).where(Comment.post_id == post_id))
    comments = result.scalars().all()
    return comments


async def update_comment(db: AsyncSession, comment_id: int, updates: CommentUpdate) -> Comment | None:
    comment = await db.get(Comment, comment_id)
    if not comment:
        return None
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(comment, field, value)
    await db.commit()
    await db.refresh(comment)
    return comment

async def delete_comment(db: AsyncSession, comment_id: int) -> bool | None:
    comment = await db.get(Comment, comment_id)
    if not comment:
        return None
    db.delete(comment)
    await db.commit()
    return True
