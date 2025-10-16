from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.tag import Tag
from app.schemas.tag import TagCreate


async def create_tag(db: AsyncSession, tag: TagCreate) -> Tag:
    new_tag = Tag(**tag.model_dump())
    db.add(new_tag)
    await db.commit()
    await db.refresh(new_tag)
    return new_tag


async def get_tag(db: AsyncSession, tag_id: int) -> Tag | None:
    tag = await db.get(Tag, tag_id)
    return tag


async def get_tag_by_name(db: AsyncSession, tag_name: str) -> Tag | None:
    result = await db.execute(select(Tag).where(Tag.name == tag_name))
    tag = await result.scalars().first()
    if not tag:
        return None
    return tag