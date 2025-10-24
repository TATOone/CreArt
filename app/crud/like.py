from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.post import get_post_by_id
from app.models.like import Like



async def like_post(user_id: int, post_id: int, db: AsyncSession) -> Like | None:
    post = await get_post_by_id(db, post_id)
    existing = await db.execute(select(Like).where(Like.post_id == post_id, Like.user_id == user_id))
    if not post or existing.scalars().one_or_none():
        return None
    new_like = Like(user_id=user_id, post_id=post_id)
    db.add(new_like)
    await db.commit()
    await db.refresh(new_like)
    return new_like


async def dislike_post(user_id: int, post_id: int, db: AsyncSession) -> bool | None:
    post = await get_post_by_id(db, post_id)
    existing = await db.execute(select(Like).where(Like.post_id == post_id, Like.user_id == user_id))
    like = existing.scalars().one_or_none()
    if not post or like is None:
        return None
    await db.delete(existing)
    await db.commit()
    return True


async def get_like_by_id(user_id: int, post_id: int, db: AsyncSession) -> Like | None:
    result = await db.execute(select(Like).where(Like.post_id == post_id, Like.user_id == user_id))
    like = result.scalars().one_or_none()
    if not like:
        return None
    return like