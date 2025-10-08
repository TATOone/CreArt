from sqlalchemy.orm import Session
from app.models.refresh_tokens import RefreshToken


def create_refresh_token(db: Session, refresh_token: str, user_id: int) -> RefreshToken:
    new_refresh_token = RefreshToken(user_id=user_id, refresh_token=refresh_token)
    db.add(new_refresh_token)
    db.commit()
    db.refresh(new_refresh_token)
    return new_refresh_token


def delete_refresh_token(db: Session, refresh_token: str) -> bool:
    token = db.query(RefreshToken).filter(RefreshToken.refresh_token == refresh_token).first()
    if not token:
        return False
    db.delete(token)
    db.commit()
    return True


def get_refresh_token(db: Session, refresh_token: str) -> RefreshToken:
    token = db.query(RefreshToken).filter(RefreshToken.refresh_token == refresh_token).first()
    return token