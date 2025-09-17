from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.follower import Follower
from app.models.user import User
from app.schemas.user import UserOut


def follow_user(db: Session, user_id: int, follower_id: int) -> Follower | None:
    user = db.query(User).filter(User.id == user_id).first()
    if not user or user.id == follower_id:
        return None
    follower = Follower(
        user_id=user.id,
        follower_id=follower_id,
    )
    db.add(follower)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
    finally:
        db.refresh(follower)
    return db.query(Follower).filter_by(follower_id=follower_id, user_id=user_id).first()


def unfollow_user(db: Session, user_id: int, follower_id: int) -> Follower | None:
    follow = db.query(Follower).filter_by(follower_id=follower_id, user_id=user_id).first()
    if not follow:
        return None
    db.delete(follow)
    db.commit()
    return follow


def get_followers_by_user(db: Session, user_id: int) -> list[UserOut]:
    followers = (
        db.query(User)
        .join(Follower, Follower.follower_id == User.id)
        .filter(Follower.user_id==user_id)
        .all()
    )
    return followers


def get_following_by_user(db: Session, user_id: int) -> list[UserOut]:
    following = (
        db.query(User)
        .join(Follower, Follower.user_id == User.id)
        .filter(Follower.follower_id==user_id)
        .all()
    )
    return following