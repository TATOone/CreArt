from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.follower import Follower
from app.models.user import User
from app.schemas.user import UserOut


async def follow_user(db: AsyncSession, user_id: int, follower_id: int) -> Follower | None:
    user = await db.get(User, user_id)
    existing = await db.execute(
        select(Follower)
        .where(Follower.user_id == user_id, Follower.follower_id == follower_id)
    )
    if not user or user.id == follower_id or existing.scalars().one_or_none():
        return None
    follower = Follower(
        user_id=user.id,
        follower_id=follower_id
    )
    db.add(follower)
    await db.commit()
    await db.refresh(follower)
    return follower


async def unfollow_user(db: AsyncSession, user_id: int, follower_id: int) -> bool | None:
    result = await db.execute(
        select(Follower)
        .where(Follower.user_id == user_id, Follower.follower_id == follower_id)
    )
    follow = result.scalars().first()
    if not follow:
        return None
    await db.delete(follow)
    await db.commit()
    return True


async def get_followers_by_user(db: AsyncSession, user_id: int) -> list[UserOut]:
    result = await db.execute(
        select(User)
        .join(Follower)
        .where(Follower.user_id == user_id)
    )
    followers = result.scalars().all()
    return followers


async def get_following_by_user(db: AsyncSession, user_id: int) -> list[UserOut]:
    result = await db.execute(
        select(User)
        .join(Follower)
        .where(Follower.follower_id == user_id)
    )
    following = result.scalars().all()
    return following