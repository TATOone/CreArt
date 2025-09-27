from fastapi import Request, APIRouter, Depends
from fastapi.templating import Jinja2Templates

from app.models.user import User
from app.schemas.user import UserOut
from app.utils import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory='app/templates')


@router.get("/me", response_model=UserOut)
def get_me(current_user:User =  Depends(get_current_user)):
    return current_user


@router.get('/dashboard')
def dashboard_home(request: Request):
    return templates.TemplateResponse('dashboard/index.html', {'request': request, 'title': 'Личный кабинет'})
