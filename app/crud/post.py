from sqlalchemy.ext.asyncio import AsyncSession

from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate
from app.utils import resolved_tags



async def create_post(db: AsyncSession, post:PostCreate, user_id: int):
    new_post = Post(**post.model_dump(exclude={'tags'}), user_id=user_id)
    new_post.tags = await resolved_tags(db, post.tags)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


async def get_post_by_id(db: AsyncSession, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()


async def get_posts(db: AsyncSession, skip: int = 0, limit: int = 100):
    return db.query(Post).offset(skip).limit(limit).all()


async def get_posts_by_category(db: AsyncSession, category: str):
    return db.query(Post).filter(Post.category == category).all()


async def update_post(db: AsyncSession, post: Post, updates: PostUpdate):
    if not post:
        return None
    for field, value in updates.model_dump(exclude={'tags'}, exclude_unset=True).items():
        setattr(post, field, value)
    if updates.tags is not None:
        new_tags = resolved_tags(db, updates.tags)
        post.tags = new_tags
    db.commit()
    db.refresh(post)
    return post


async def delete_post(db: AsyncSession, post_id: int):
    post =  get_post_by_id(db, post_id)
    if not post:
        return None
    db.delete(post)
    db.commit()
    return True