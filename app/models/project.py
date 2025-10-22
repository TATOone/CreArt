from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime, Enum
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.type import ProjectStatusTypes

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    status = Column(Enum(ProjectStatusTypes), default=ProjectStatusTypes.ACTIVE, server_default='active')
    progress = Column(Integer, default=0)
    members = Column(Text, nullable=True)
    avatar_url = Column(String(255), nullable=True)
    goal1 = Column(String(255), nullable=True)
    goal2 = Column(String(255), nullable=True)
    goal3 = Column(String(255), nullable=True)
    stage_image_1 = Column(String(255), nullable=True)
    stage_desc_1 = Column(Text, nullable=True)
    stage_image_2 = Column(String(255), nullable=True)
    stage_desc_2 = Column(Text, nullable=True)
    stage_image_3 = Column(String(255), nullable=True)
    stage_desc_3 = Column(Text, nullable=True)
    sketch_image_1 = Column(String(255), nullable=True)
    sketch_image_2 = Column(String(255), nullable=True)
    sketch_image_3 = Column(String(255), nullable=True)
    sketch_image_4 = Column(String(255), nullable=True)
    result_image_1 = Column(String(255), nullable=True)
    result_image_2 = Column(String(255), nullable=True)
    result_image_3 = Column(String(255), nullable=True)
    contact_email = Column(String(255), nullable=True)
    contact_instagram = Column(String(255), nullable=True)
    contact_telegram = Column(String(255), nullable=True)
    contact_behance = Column(String(255), nullable=True)
    contact_vk = Column(String(255), nullable=True)

    user = relationship('User', back_populates='projects')