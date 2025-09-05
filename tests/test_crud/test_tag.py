from sqlalchemy.orm import Session

from tests.conftest import db_session, test_tag
from app.models.tag import Tag
from app.schemas.tag import TagCreate
from app.crud.tag import get_tag, get_tag_by_name, create_tag


def test_create_tag(db_session: Session, test_tag: TagCreate):
    tags_in_db = db_session.query(Tag).all()

    assert len(tags_in_db) == 1
    assert tags_in_db[0].id == test_tag.id
    assert tags_in_db[0].name == test_tag.name


def test_get_tag(db_session: Session, test_tag: TagCreate):
    new_tag = get_tag(db_session, test_tag.id)

    assert new_tag.id == test_tag.id
    assert new_tag.name == test_tag.name


def test_get_tag_by_name(db_session: Session, test_tag: TagCreate):
    new_tag = get_tag_by_name(db_session, test_tag.name)

    assert new_tag.id == test_tag.id
    assert new_tag.name == test_tag.name

