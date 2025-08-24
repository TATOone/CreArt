from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, Text, DateTime
from sqlalchemy.orm import relationship, backref

from app.core.database import Base


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))
    parent_id = Column(Integer, ForeignKey('comments.id'))
    content = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)

    post = relationship('Post', back_populates='comments')
    user = relationship('User', back_populates='comments')

    replies = relationship('Comment', backref=backref('parent', remote_side=[id]))