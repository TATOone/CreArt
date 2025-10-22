from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.project import create_project, get_project_by_id, update_project, delete_project, get_projects_by_user_id
from app.crud.user import get_user_by_id
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectOut, ProjectUpdate
from app.utils import get_current_user
from app.utils import get_db


router = APIRouter(prefix='/projects', tags=['projects'], dependencies=[Depends(get_current_user)])


@router.post('/', response_model=ProjectOut)
async def create_project_api(project:ProjectCreate, db: AsyncSession=Depends(get_db), user:User=Depends(get_current_user)) -> ProjectOut:
    try:
        new_project = await create_project(db, project, user.id)
    except (IntegrityError, SQLAlchemyError) as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.detail)
    return new_project


@router.get('/', response_model=list[ProjectOut])
async def get_own_projects(db: AsyncSession=Depends(get_db), user: User=Depends(get_current_user)) -> list[ProjectOut]:
    result = await get_projects_by_user_id(db, user.id)
    if not result:
        return []
    return result


@router.get('/{project_id}', response_model=ProjectOut)
async def get_project_by_id_api(project_id: int, db: AsyncSession=Depends(get_db), user: User = Depends(get_current_user)) -> ProjectOut:
    result = await get_project_by_id(db, project_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Проект не найден!')
    if result.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Нет доступа к этому проекту')
    return result


@router.get('/user/{user_id}', response_model=list[ProjectOut])
async def get_projects_by_user_api(user_id: int, db: AsyncSession=Depends(get_db)) -> list[ProjectOut]:
    user = await get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такого пользователя не существует!')
    result = await get_projects_by_user_id(db, user_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='У этого пользователя нет проектов!')
    return result


@router.patch('/{project_id}', response_model=ProjectOut)
async def update_project_api(project_id: int, project_updates: ProjectUpdate, db: AsyncSession=Depends(get_db), user: User=Depends(get_current_user)) -> ProjectOut:
    project = await get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такого проекта не существует!')
    if project.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Нет доступа к этому проекту!')
    try:
        result = await update_project(db, project, project_updates)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Такой проект уже существует!')
    return result


@router.delete('/{project_id}')
async def delete_project_api(project_id: int, db: AsyncSession=Depends(get_db), user: User = Depends(get_current_user)):
    project = await get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Такого проекта не существует!')
    if project.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Нет доступа к этому проекту!')
    await delete_project(db, project_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

