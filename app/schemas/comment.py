from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    pass


class CommentUpdate(CommentBase):
    content: Optional[str] = None
    parent_id: Optional[int] = None


class CommentOut(CommentBase):
    id: int
    content: str
    parent_id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True