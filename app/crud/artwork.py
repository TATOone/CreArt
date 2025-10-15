from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.artwork import Artwork
from app.schemas.artwork import ArtworkCreate, ArtworkUpdate


async def create_artwork(db: AsyncSession, artwork: ArtworkCreate) -> Artwork:
    new_artwork = Artwork(**artwork.model_dump())
    db.add(new_artwork)
    await db.commit()
    await db.refresh(new_artwork)
    return new_artwork


async def get_artwork_by_id(db: AsyncSession, artwork_id: int) -> Artwork | None:
    artwork = await db.get(Artwork, artwork_id)
    return artwork


async def get_artworks_by_user_id(db: AsyncSession, user_id: int) -> list[Artwork]:
    result = await db.execute(select(Artwork).where(Artwork.user_id == user_id))
    artworks = result.scalars().all()
    return artworks


async def get_artworks_by_tag(db: AsyncSession, tag: str) -> list[Artwork]:
    result = await db.execute(select(Artwork).where(Artwork.tags.contains(tag)))
    artworks = result.scalars().all()
    return artworks


async def update_artwork(db: AsyncSession, artwork_id: int, updates: ArtworkUpdate) -> Artwork | None:
    artwork = await db.get(Artwork, artwork_id)
    if not artwork:
        return None
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(artwork, field, value)
    await db.commit()
    await db.refresh(artwork)
    return artwork


async def delete_artwork(db: AsyncSession, artwork_id: int) -> bool | None:
    artwork = await db.get(Artwork, artwork_id)
    if not artwork:
        return None
    db.delete(artwork)
    await db.commit()
    return True