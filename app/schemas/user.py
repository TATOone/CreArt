from datetime import datetime
from enum import Enum
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
    username: str
    first_name: str
    last_name: str
    bio: str
    profession: str
    location: str
    company: str
    short_description: str
    achievements: str
    city: str
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


