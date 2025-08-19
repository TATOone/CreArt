from fastapi import Request, APIRouter
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory='app/templates')

@router.get('/dashboard')
def dashboard_home(request: Request):
    return templates.TemplateResponse('dashboard/index.html', {'request': request, 'title': 'Личный кабинет'})
