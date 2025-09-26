from sqlalchemy.orm import Session

from app.models.type import RoleType
from app.utils import hash_password
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


def create_user(db: Session, user: UserCreate):
    password_hash = hash_password(user.password)
    new_user = User(**user.model_dump(exclude={'password'}), password_hash=password_hash, role=RoleType.USER)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def update_user(db: Session, user: User, updates: UserUpdate):
    if not user:
        return None
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int):
    deleted = db.query(User).filter(User.id == user_id).delete()
    db.commit()
    return deleted


