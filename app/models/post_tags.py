from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql.schema import Table

from app.core.database import Base


post_tags = Table(
    'post_tags',
    Base.metadata,
    Column('tag_id', ForeignKey('tags.id'), primary_key=True),
    Column('post_id', ForeignKey('posts.id'), primary_key=True)
)