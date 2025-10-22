from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user_settings import UserSettings
from app.schemas.user_settings import UserSettingsCreate, UserSettingsUpdate


async def create_user_settings(db: AsyncSession, settings: UserSettingsCreate, user_id: int) -> UserSettings:
    """Создать настройки пользователя"""
    new_settings = UserSettings(**settings.model_dump(), user_id=user_id)
    db.add(new_settings)
    await db.commit()
    await db.refresh(new_settings)
    return new_settings


async def get_user_settings_by_user_id(db: AsyncSession, user_id: int) -> UserSettings | None:
    """Получить настройки пользователя по user_id"""
    result = await db.execute(select(UserSettings).where(UserSettings.user_id == user_id))
    return result.scalar_one_or_none()


async def update_user_settings(db: AsyncSession, settings: UserSettings, updates: UserSettingsUpdate) -> UserSettings | None:
    """Обновить настройки пользователя"""
    if not settings:
        return None
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(settings, field, value)
    try:
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        raise e
    await db.refresh(settings)
    return settings


async def delete_user_settings(db: AsyncSession, user_id: int) -> bool | None:
    """Удалить настройки пользователя"""
    result = await db.execute(select(UserSettings).where(UserSettings.user_id == user_id))
    settings = result.scalar_one_or_none()
    
    if not settings:
        return None
    
    await db.delete(settings)
    await db.commit()
    return True
