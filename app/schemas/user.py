from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    first_name: str | None = None
    last_name: str | None = None


class UserCreate(UserBase):
    username: str
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None
    profession: Optional[str] = None
    location: Optional[str] = None
    company: Optional[str] = None
    short_description: Optional[str] = None
    achievements: Optional[str] = None
    city: Optional[str] = None
    birth_date: Optional[datetime] = None
    specialization: Optional[str] = None
    email: Optional[str] = None
    biography: Optional[str] = None
    skills: Optional[str] = None
    skills_level: Optional[Enum] = None
    teach_skills: Optional[str] = None
    learn_skills: Optional[str] = None
    collaboration_interests: Optional[str] = None
    current_projects: Optional[str] = None
    vk_link: Optional[str] = None
    behance_link: Optional[str] = None
    youtube_link: Optional[str] = None
    telegram_link: Optional[str] = None
    pinterest_link: Optional[str] = None
    last_publications_count: Optional[int] = None
    total_likes: Optional[int] = None
    avatar: Optional[str] = None
    role: Optional[Enum] = None
    is_active: Optional[bool] = None


class UserPublic(UserBase):
    username: str
    bio: Optional[str] = None
    vk_link: Optional[str] = None
    behance_link: Optional[str] = None
    youtube_link: Optional[str] = None
    telegram_link: Optional[str] = None
    pinterest_link: Optional[str] = None
    short_description: Optional[str] = None
    collaboration_interests: Optional[str] = None
    current_projects: Optional[str] = None
    specialization: Optional[str] = None

    class Config:
        orm_mode = True
        from_attributes = True


class UserOut(UserPublic):
    email:str
    role: Enum
    is_active: bool
    profession: Optional[str] = None
    location: Optional[str] = None
    company: Optional[str] = None
    achievements: Optional[str] = None
    city: Optional[str] = None
    birth_date: Optional[datetime] = None
    email: Optional[str] = None
    biography: Optional[str] = None
    skills: Optional[str] = None
    skills_level: Optional[Enum] = None
    teach_skills: Optional[str] = None
    learn_skills: Optional[str] = None
    last_publications_count: Optional[int] = None
    total_likes: Optional[int] = None
    avatar: Optional[str] = None
    role: Optional[Enum] = None
    is_active: Optional[bool] = None

