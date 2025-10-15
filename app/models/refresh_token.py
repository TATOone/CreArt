from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship

from app.core.database import Base


class RefreshToken(Base):
    __tablename__ = 'refresh_tokens'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    refresh_token = Column(String(512), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)

    user = relationship('User', back_populates='refresh_tokens')