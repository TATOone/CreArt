from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.user import get_user_by_id
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate


async def create_project(db: AsyncSession, project: ProjectCreate, user_id: int) -> Project:
    """Создать новый проект"""
    new_project = Project(**project.model_dump(), user_id=user_id)
    db.add(new_project)
    await db.commit()
    await db.refresh(new_project)
    return new_project


async def get_project_by_id(db: AsyncSession, project_id: int) -> Project | None:
    """Получить проект по ID"""
    result = await db.execute(select(Project).where(Project.id == project_id))
    return result.scalar_one_or_none()


async def get_projects_by_user_id(db: AsyncSession, user_id: int) -> list[Project] | None:
    """Получить все проекты пользователя"""
    result = await db.execute(select(Project).where(Project.user_id == user_id))
    projects = result.scalars().all()
    if not projects:
        return None
    return projects


async def get_projects_by_status(db: AsyncSession, status: str) -> list[Project] | None:
    """Получить проекты по статусу"""
    result = await db.execute(select(Project).where(Project.status == status))
    projects = result.scalars().all()
    if not projects:
        return None
    return projects


async def update_project(db: AsyncSession, project: Project, updates: ProjectUpdate) -> Project | None:
    """Обновить проект"""
    if not project:
        return None
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(project, field, value)
    try:
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        raise e
    await db.refresh(project)
    return project


async def delete_project(db: AsyncSession, project_id: int) -> bool | None:
    """Удалить проект"""
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    
    if not project:
        return None
    
    await db.delete(project)
    await db.commit()
    return True
