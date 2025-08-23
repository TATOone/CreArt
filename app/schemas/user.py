from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    first_name: str
    last_name: str
    bio: str
    profession: str
    location: str
    company: str
    created_at: datetime
    short_description: str
    achievements: str
    city:str
    birth_date: datetime
    specialization: str
    email: str
    biography: str
    skills: str
    skills_level: Enum
    teach_skills: str
    learn_skills: str
    collaboration_interests: str
    current_projects: str
    vk_link: str
    behance_link: str
    youtube_link: str
    telegram_link: str
    pinterest_link: str
    last_publications_count: int
    total_likes: int
    avatar: str
    role: Enum
    is_active: bool

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


