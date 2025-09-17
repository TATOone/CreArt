from pydantic import BaseModel
from datetime import datetime


class FollowerBase(BaseModel):
    user_id: int
    follower_id: int


class FollowerCreate(FollowerBase):
    pass

class FollowerOut(FollowerBase):
    id:int
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True

