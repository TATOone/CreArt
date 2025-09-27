from fastapi import Depends, HTTPException, APIRouter, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.user import User
from app.utils import verify_password, create_access_token

router = APIRouter()
templates = Jinja2Templates("templates")

def get_db():
    session: Session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm, db: Session=Depends(get_db)):
    username = form_data.username
    password = form_data.password
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Неверное имя пользователя!")
    if not verify_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Неверный пароль!")
    token = create_access_token(data={'sub': user.id, 'username': username, 'role': user.role.value})
    return {'token': token, 'token_type': 'bearer'}


