from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.post_tags import post_tags


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True, index=True)

    posts = relationship("Post", secondary=post_tags, back_populates="tags")