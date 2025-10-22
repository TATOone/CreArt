from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.type import *


class UserSettings(Base):
    __tablename__ = 'user_settings'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    theme = Column(Enum(ThemeType), nullable=True, default=ThemeType.DARK, server_default='dark')
    notifications_enabled = Column(Boolean, nullable=False, default=True)
    language = Column(String(10), nullable=True, default='en')

    user = relationship('User', back_populates='settings')
