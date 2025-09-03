from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, DateTime
from sqlalchemy.orm import relationship

from app.core.database import Base


class Like(Base):
    __tablename__ = 'likes'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))
    created_at = Column(DateTime, default=datetime.now)

    post = relationship('Post', foreign_keys=[post_id], back_populates='likes')
    user = relationship('User', foreign_keys=[user_id], back_populates='likes')
