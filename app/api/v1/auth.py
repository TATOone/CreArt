from fastapi import Depends, HTTPException, APIRouter, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.crud.user import create_user, get_user_by_username, get_user_by_email
from app.models.user import User
from app.core.security_utils import verify_password, create_access_token, create_refresh_token
from app.schemas.token import RefreshRequest
from app.core.config import settings
from app.schemas.user import UserCreate, UserOut

router = APIRouter()
templates = Jinja2Templates("templates")

def get_db():
    session: Session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@router.post("/login", response_model=None)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session=Depends(get_db)):
    username = form_data.username
    password = form_data.password
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверное имя пользователя!")
    if not verify_password(password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный пароль!")
    access_token = create_access_token(data={'sub': str(user.id), 'username': username, 'role': user.role.value})
    refresh_token = create_refresh_token(data={'sub': str(user.id)})
    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'bearer'
    }

@router.post("/refresh")
def refresh(request: RefreshRequest, db: Session=Depends(get_db)):
    refresh_token = request.refresh_token
    try:
        user_id = int(jwt.decode(refresh_token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM]).get('sub'))
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Срок годности токена истёк. Залогиньтесь заново!")
    finally:
        print(jwt.decode(refresh_token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM]))
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный id пользователя!")
    access_token = create_access_token(data={'sub': user.id, 'username': user.username, 'role': user.role.value})
    return {
        'access_token': access_token,
        'token_type': 'bearer'
    }


@router.post('/register', response_model=UserOut)
def register( user_data: UserCreate, db: Session=Depends(get_db)):
    if get_user_by_username(db, user_data.username):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail="Это имя занято попробуйте другое!"
        )
    if get_user_by_email(db, user_data.email):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с такой электронной почтой уже зарегистрирован!"
                   "\nПопробуйте залогиниться."
        )
    user = create_user(db, user_data)
    return user





