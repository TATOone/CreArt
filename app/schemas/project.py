from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.models.type import ProjectStatusTypes


class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: Optional[ProjectStatusTypes] = ProjectStatusTypes.ACTIVE
    progress: Optional[int] = 0
    members: Optional[str] = None
    avatar_url: Optional[str] = None
    goal1: Optional[str] = None
    goal2: Optional[str] = None
    goal3: Optional[str] = None
    stage_image_1: Optional[str] = None
    stage_desc_1: Optional[str] = None
    stage_image_2: Optional[str] = None
    stage_desc_2: Optional[str] = None
    stage_image_3: Optional[str] = None
    stage_desc_3: Optional[str] = None
    sketch_image_1: Optional[str] = None
    sketch_image_2: Optional[str] = None
    sketch_image_3: Optional[str] = None
    sketch_image_4: Optional[str] = None
    result_image_1: Optional[str] = None
    result_image_2: Optional[str] = None
    result_image_3: Optional[str] = None
    contact_email: Optional[str] = None
    contact_instagram: Optional[str] = None
    contact_telegram: Optional[str] = None
    contact_behance: Optional[str] = None
    contact_vk: Optional[str] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ProjectStatusTypes] = None
    progress: Optional[int] = None
    members: Optional[str] = None
    avatar_url: Optional[str] = None
    goal1: Optional[str] = None
    goal2: Optional[str] = None
    goal3: Optional[str] = None
    stage_image_1: Optional[str] = None
    stage_desc_1: Optional[str] = None
    stage_image_2: Optional[str] = None
    stage_desc_2: Optional[str] = None
    stage_image_3: Optional[str] = None
    stage_desc_3: Optional[str] = None
    sketch_image_1: Optional[str] = None
    sketch_image_2: Optional[str] = None
    sketch_image_3: Optional[str] = None
    sketch_image_4: Optional[str] = None
    result_image_1: Optional[str] = None
    result_image_2: Optional[str] = None
    result_image_3: Optional[str] = None
    contact_email: Optional[str] = None
    contact_instagram: Optional[str] = None
    contact_telegram: Optional[str] = None
    contact_behance: Optional[str] = None
    contact_vk: Optional[str] = None


class ProjectOut(ProjectBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True
