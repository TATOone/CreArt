from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate
from app.utils import resolved_tags



async def create_post(db: AsyncSession, post:PostCreate, user_id: int):
    new_post = Post(**post.model_dump(exclude={'tags'}), user_id=user_id)
    try:
        new_post.tags = await resolved_tags(db, post.tags)
        db.add(new_post)
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        raise e
    await db.refresh(new_post)
    return new_post


async def get_post_by_id(db: AsyncSession, post_id: int) -> Post | None:
    post = await db.get(Post, post_id)
    return post


async def get_posts_by_user(db: AsyncSession, user_id: int) -> list[Post]:
    result = await db.execute(select(Post).where(Post.user_id == user_id))
    posts = result.scalars().all()
    return posts


async def get_posts_by_category(db: AsyncSession, category: str) -> list[Post]:
    result = await db.execute(select(Post).where(Post.category == category))
    posts = result.scalars().all()
    return posts


async def update_post(db: AsyncSession, post: Post, updates: PostUpdate) -> Post | None:
    if not post:
        return None
    for field, value in updates.model_dump(exclude={'tags'}, exclude_unset=True).items():
        setattr(post, field, value)
    try:
        if updates.tags is not None:
            new_tags = await resolved_tags(db, updates.tags)
            post.tags = new_tags
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        raise e
    await db.refresh(post)
    return post


async def delete_post(db: AsyncSession, post_id: int) -> bool | None:
    post = await db.get(Post, post_id)
    if not post:
        return None
    await db.delete(post)
    await db.commit()
    return True