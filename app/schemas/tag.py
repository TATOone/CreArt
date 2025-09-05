from typing import Optional
from pydantic import BaseModel


class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

# class TagUpdate(BaseModel):       # Не уверен нужно будет или нет.
#     name: Optional[str] = None

class TagOut(TagBase):
    id: int
    class Config:
        orm_mode = True
        from_attributes = True