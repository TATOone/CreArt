from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

from app.schemas.tag import TagCreate


class PostBase(BaseModel):
    title: str
    content: str
    category: str

class PostCreate(PostBase):
    is_pinned: Optional[bool] = False
    tags: List[TagCreate] = []

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    is_pinned: Optional[bool] = False
    tags: Optional[List[TagCreate]] = None

class PostOut(PostBase):
    id: int
    user_id: int
    created_at: datetime
    is_pinned: bool
    tags: List[TagCreate] = []

    class Config:
        from_attributes = True
        orm_mode = True
