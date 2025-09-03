from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum, Text
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.follower import Follower
from app.models.type import SkillLevelType, RoleType


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    bio = Column(Text, nullable=True)
    profession = Column(String(100), nullable=True)
    location = Column(String(100), nullable=True)
    company = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    short_description = Column(String(255), nullable=True)
    achievements = Column(Text, nullable=True)
    city = Column(String(100), nullable=True)
    birth_date = Column(DateTime, nullable=True)
    specialization = Column(String(100), nullable=True)
    email = Column(String(100), nullable=True)
    biography = Column(String(255), nullable=True)
    skills = Column(String(255), nullable=True)
    skill_level = Column(Enum(SkillLevelType), default=SkillLevelType.BEGINNER, server_default='beginner', nullable=True)
    teach_skills = Column(String(255), nullable=True)
    learn_skills = Column(String(255), nullable=True)
    collaboration_interests = Column(String(255), nullable=True)
    current_projects = Column(String(255), nullable=True)
    vk_link = Column(String(255), nullable=True)
    behance_link = Column(String(255), nullable=True)
    youtube_link = Column(String(255), nullable=True)
    telegram_link = Column(String(255), nullable=True)
    pinterest_link = Column(String(255), nullable=True)
    last_publications_count = Column(Integer, nullable=True)
    total_likes = Column(Integer, nullable=True)
    avatar = Column(String(255), nullable=True)
    role = Column(Enum(RoleType), nullable=False, default=RoleType.USER, server_default='user')
    is_active = Column(Boolean, nullable=False, default=True)

    settings = relationship('UserSettings', back_populates='user', uselist=True)
    artworks = relationship('Artwork', back_populates='user', uselist=True)
    comments = relationship('Comment', back_populates='user', uselist=True)
    followers = relationship('Follower',foreign_keys=[Follower.user_id], back_populates='user', uselist=True)
    following = relationship('Follower', foreign_keys=[Follower.follower_id], back_populates='followers', uselist=True)
    posts = relationship('Post', back_populates='user', uselist=True)
    likes = relationship('Like', back_populates='user', uselist=True)
    projects = relationship('Project', back_populates='user', uselist=True)
