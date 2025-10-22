from typing import Optional
from pydantic import BaseModel
from app.models.type import ThemeType


class UserSettingsBase(BaseModel):
    theme: Optional[ThemeType] = ThemeType.DARK
    notifications_enabled: Optional[bool] = True
    language: Optional[str] = 'en'


class UserSettingsCreate(UserSettingsBase):
    pass


class UserSettingsUpdate(BaseModel):
    theme: Optional[ThemeType] = None
    notifications_enabled: Optional[bool] = None
    language: Optional[str] = None


class UserSettingsOut(UserSettingsBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
        from_attributes = True
