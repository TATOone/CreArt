from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserOut, UserUpdate
from app.utils import get_current_user
from app.utils import get_db

router = APIRouter(prefix='/users', tags=['users'], dependencies=[Depends(get_current_user)])


@router.get("/me", response_model=UserOut)
async def get_me(current_user:User = Depends(get_current_user)):
    return current_user
