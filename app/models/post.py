from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, Text, Boolean, DateTime
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.post_tags import post_tags


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    category = Column(String(100), nullable=False)
    likes_count = Column(Integer, default=0, server_default='0')
    comments_count = Column(Integer, default=0, server_default='0')
    is_pinned = Column(Boolean, default=False, server_default='0')

    user = relationship('User', back_populates='posts')
    comments = relationship('Comment', back_populates='post', cascade='all, delete-orphan')
    likes = relationship('Like', back_populates='post', cascade='all, delete-orphan')
    tags = relationship('Tag', secondary=post_tags, back_populates='posts')