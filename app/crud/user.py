from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


def create_user(db: Session, user: UserCreate):
    new_user = User(
        username = user.username,
        first_name = user.first_name,
        last_name = user.last_name,
        bio = user.bio,
        profession = user.profession,
        location = user.location,
        company = user.company,
        created_at = user.created_at,
        short_description = user.short_description,
        achievements = user.achievements,
        city = user.city,
        birth_date = user.birth_date,
        specialization = user.specialization,
        email = user.email,
        biography = user.biography,
        skills = user.skills,
        skill_level = user.skill_level,
        teach_skills = user.teach_skills,
        learn_skills = user.learn_skills,
        collaboration_interests = user.collaboration_interests,
        current_projects = user.current_projects,
        vk_link = user.vk_link,
        behance_link = user.behance_link,
        youtube_link = user.youtube_link,
        telegram_link = user.telegram_link,
        pinterest_link = user.pinterest_link,
        last_publications_count = user.last_publications_count,
        total_likes = user.total_likes,
        avatar = user.avatar,
        role = user.role,
        is_active = user.is_active,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def

