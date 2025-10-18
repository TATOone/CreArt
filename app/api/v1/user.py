from fastapi import APIRouter, Depends

from app.models.user import User
from app.schemas.user import UserOut
from app.utils import get_current_user


router = APIRouter()


@router.get("/me", response_model=UserOut)
async def get_me(current_user:User =  Depends(get_current_user)):
    return current_user
