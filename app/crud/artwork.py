from sqlalchemy.orm import Session

from app.models.artwork import Artwork
from app.schemas.artwork import ArtworkCreate, ArtworkUpdate


def create_artwork(db: Session, artwork: ArtworkCreate) -> Artwork:
    new_artwork = Artwork(**artwork.model_dump())
    db.add(new_artwork)
    db.commit()
    db.refresh(new_artwork)
    return new_artwork


def get_artwork_by_id(db: Session, artwork_id: int) -> Artwork:
    artwork = db.query(Artwork).filter(Artwork.id == artwork_id).first()
    return artwork


def get_artworks_by_user(db: Session, user_id: int) -> list[Artwork]:
    artworks = db.query(Artwork).filter(Artwork.user_id == user_id).all()
    return artworks


def get_artworks_by_tag(db: Session, tag: str) -> list[Artwork]:
    artworks = db.query(Artwork).filter(Artwork.tags.contains(tag)).all()
    return artworks


def update_artwork(db: Session,artwork_id: int, updates: ArtworkUpdate) -> Artwork:
    artwork = get_artwork_by_id(db, artwork_id)
    if not artwork:
        return None
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(artwork, field, value)
    db.commit()
    db.refresh(artwork)
    return artwork


def delete_artwork(db: Session, artwork_id: int) -> None:
    artwork = get_artwork_by_id(db, artwork_id)
    if not artwork:
        return None
    db.delete(artwork)
    db.commit()
    return True