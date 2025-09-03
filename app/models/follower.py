from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, DateTime
from sqlalchemy.orm import relationship

from app.core.database import Base

class Follower(Base):
    __tablename__ = 'followers'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    follower_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.now)

    user = relationship('User', foreign_keys=[user_id], back_populates='followers')
    followers = relationship('User', foreign_keys=[follower_id], back_populates='following')