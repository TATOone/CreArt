from datetime import datetime

from pydantic import BaseModel
from typing import Optional, List

from app.schemas.tag import TagCreate


class ArtworkBase(BaseModel):
    title: str
    description: str
    image_path: str



class ArtworkCreate(ArtworkBase):
    tags: Optional[List[TagCreate]] = None
    likes_count: Optional[int] = None
    shares_count: Optional[int] = None
    favorites_count: Optional[int] = None
    is_public: Optional[bool] = None
    allow_comments: Optional[bool] = None


class ArtworkUpdate(ArtworkBase):
    title: Optional[str] = None
    description: Optional[str] = None
    image_path: Optional[str] = None
    tags: Optional[List[TagCreate]] = None
    likes_count: Optional[int] = None
    shares_count: Optional[int] = None
    favorites_count: Optional[int] = None
    is_public: Optional[bool] = None
    allow_comments: Optional[bool] = None


class ArtworkOut(BaseModel):
    id: str
    user_id: str
    created_at: datetime
    tags: List[TagCreate]
    likes_count: int
    shares_count: int
    favorites_count: int
    is_public: bool
    allow_comments: bool

    class Config:
        orm_mode = True
        from_attributes = True
