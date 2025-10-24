from fastapi import APIRouter, Depends, HTTPException, Response, status

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.user_settings import create_user_settings, get_user_settings_by_user_id, update_user_settings, delete_user_settings
from app.models.user import User
from app.schemas.user_settings import UserSettingsCreate, UserSettingsOut, UserSettingsUpdate
from app.utils import get_current_user
from app.utils import get_db


router = APIRouter(prefix='/user_settings', tags=['user_settings'], dependencies=[Depends(get_current_user)])


@router.post('/me', response_model=UserSettingsOut)
async def create_user_settings_api(settings:UserSettingsCreate, db: AsyncSession=Depends(get_db), user: User=Depends(get_current_user)) -> UserSettingsOut:
    try:
        return await create_user_settings(db, settings, user.id)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='У этого пользователя уже есть настройки, попробуйте их обновить!')

@router.get('/me', response_model=UserSettingsOut)
async def get_user_settings_by_user_id_api(db: AsyncSession=Depends(get_db), user: User=Depends(get_current_user)) -> UserSettingsOut:
    settings = await get_user_settings_by_user_id(db, user.id)
    if not settings:
        default_settings = UserSettingsCreate()
        settings = await create_user_settings(db, default_settings, user.id)
    return settings


@router.patch('/me', response_model=UserSettingsOut)
async def update_user_settings_api(settings_updates: UserSettingsUpdate, db: AsyncSession=Depends(get_db), user: User=Depends(get_current_user)) -> UserSettingsOut:
    settings = await get_user_settings_by_user_id(db, user.id)
    if not settings:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Настройки не найдены!')
    return await update_user_settings(db, settings, settings_updates)


@router.delete('/me')
async def delete_user_settings_api(db: AsyncSession=Depends(get_db), user: User=Depends(get_current_user)):
    result = await delete_user_settings(db, user.id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Настройки не найдены!')
    return Response(status_code=status.HTTP_204_NO_CONTENT)