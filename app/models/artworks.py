from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, Text, Boolean, DateTime
from sqlalchemy.orm import relationship

from app.core.database import Base


class Artwork(Base):
    __tablename__ = 'artworks'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    tags = Column(String(255), nullable=True)
    image_path = Column(String(255), nullable=True)
    likes_count = Column(Integer, default=0, server_default='0', nullable=True)
    shares_count = Column(Integer, default=0, server_default='0', nullable=True)
    favorites_count = Column(Integer, default=0, server_default='0', nullable=True)
    is_public = Column(Boolean, default=True, server_default='1', nullable=True)
    allow_comments = Column(Boolean, default=True, server_default='1', nullable=True)
    created_at = Column(DateTime, default=datetime.now, nullable=True)

    user = relationship('User', back_populates='artworks')