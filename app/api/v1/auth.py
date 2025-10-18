from fastapi import Depends, HTTPException, APIRouter, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import SessionLocal
from app.core.config import settings
from app.core.security_utils import verify_password, create_access_token, create_refresh_token

from app.crud.refresh_token import delete_refresh_token, create_refresh_token_in_db, get_refresh_token
from app.crud.user import create_user, get_user_by_id, get_user_by_username, get_user_by_email
from app.models.user import User
from app.schemas.token import RefreshRequest
from app.schemas.user import UserCreate, UserOut
from app.utils import get_current_user


router = APIRouter()
templates = Jinja2Templates("templates")

async def get_db():
    async with SessionLocal() as db:
        yield db


@router.post("/login", response_model=None)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession=Depends(get_db)):
    username = form_data.username
    password = form_data.password
    user = await get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверное имя пользователя!")
    if not verify_password(password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный пароль!")
    access_token = create_access_token(data={'sub': str(user.id), 'username': username, 'role': user.role.value})
    refresh_token = create_refresh_token(data={'sub': str(user.id)})
    await create_refresh_token_in_db(db, refresh_token, user.id)
    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'bearer'
    }


@router.post("/refresh")
async def refresh(request: RefreshRequest, db: AsyncSession=Depends(get_db)):
    refresh_token = await get_refresh_token(db, request.refresh_token)
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Срок годности токена истёк. Залогиньтесь заново!")
    user = await get_user_by_id(db, refresh_token.user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный id пользователя!")
    access_token = create_access_token(data={'sub': user.id, 'username': user.username, 'role': user.role.value})
    return {
        'access_token': access_token,
        'token_type': 'bearer'
    }


@router.post('/register', response_model=UserOut)
async def register( user_data: UserCreate, db: AsyncSession=Depends(get_db)):
    if await get_user_by_username(db, user_data.username):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail="Это имя занято попробуйте другое!"
        )
    if await get_user_by_email(db, user_data.email):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с такой электронной почтой уже зарегистрирован!"
                   "\nПопробуйте залогиниться."
        )
    user = await create_user(db, user_data)
    return user


@router.post('/logout')
async def logout(request: RefreshRequest, db: AsyncSession=Depends(get_db)):
    token = request.refresh_token
    if not await delete_refresh_token(db, token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Такого токена нет в базе!'
        )
    return {'detail': 'Вы успешно разлогинились:)'}





