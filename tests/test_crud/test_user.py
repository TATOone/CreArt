from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserUpdate
from tests.conftest import db_session, test_user
from app.crud.user import get_user_by_id, update_user, delete_user


def test_create_user(db_session: Session, test_user) -> None:
    users_in_db = db_session.query(User).all()

    assert len(users_in_db) == 1
    assert users_in_db[0].username == test_user.username


def test_get_user(db_session: Session, test_user) -> None:
    user = get_user_by_id(db_session, test_user.id)

    assert user is not None
    assert user.username == test_user.username


def test_update_user(db_session: Session, test_user) -> None:
    update_data = UserUpdate(username='updated')
    update_user(db_session, test_user, update_data)
    user = db_session.query(User).filter_by(id=test_user.id).first()

    assert user.username == update_data.username
    assert user.email == test_user.email


def test_delete_user(db_session: Session, test_user) -> None:
    deleted = delete_user(db_session, test_user.id)
    user = db_session.query(User).filter_by(id=test_user.id).first()

    assert user is None
    assert deleted == 1


def test_get_unknown_user(db_session: Session, test_user) -> None:
    user = get_user_by_id(db_session, 2)

    assert user is None


def test_update_unknown_user(db_session: Session, test_user) -> None:
    update_data = UserUpdate(username='updated')
    user = get_user_by_id(db_session, 2)

    assert update_user(db_session, user, update_data) is None


def test_delete_unknown_user(db_session: Session, test_user) -> None:
    deleted = delete_user(db_session, 2)

    assert deleted == 0