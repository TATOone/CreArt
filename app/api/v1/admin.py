from fastapi import Request, APIRouter
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory='app/templates')

@router.get('/admin')
async def admin_home(request: Request):
    return templates.TemplateResponse('admin/index.html', {'request': request, 'title': 'Админка'})
