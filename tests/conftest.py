from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pytest import fixture

from app.core.database import Base
from app.models.types import SkillLevelType, RoleType
from app.models.user import User



@fixture(scope='function')
def db_session():
    engine = create_engine('sqlite:///:memory:', echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield session
    session.close()

@fixture(scope='function')
def test_user(db_session):
    test_user = User(
        username='TestUser',
        first_name='TestFirstName',
        last_name='TestLastName',
        bio='TestBio',
        profession='TestProfession',
        location='TestLocation',
        company='TestCompany',
        created_at=datetime(2024,1,1),
        short_description='TestShortDescription',
        achievements='TestAchievements',
        city='TestCity',
        birth_date=datetime(1997,6,10),
        specialization='TestSpecialization',
        email='Test@Email.com',
        biography='TestBiography',
        skills='TestSkill1, TestSkill2',
        skill_level=SkillLevelType.BEGINNER,
        teach_skills='TestTeachSkill1, TestTeachSkill2',
        learn_skills='TestLearnSkill1, TestLearnSkill2',
        collaboration_interests='TestCollaborationInterest1, TestCollaborationInterest2',
        current_projects='TestProjects',
        vk_link='TestVKLink',
        behance_link='TestBehanceLink',
        youtube_link='TestYoutubeLink',
        telegram_link='TestTelegramLink',
        pinterest_link='TestPinterestLink',
        last_publications_count=1,
        total_likes=1,
        avatar='TestAvatar',
        role=RoleType.USER,
        is_active=True
)
    db_session.add(test_user)
    db_session.commit()
    db_session.refresh(test_user)
    return test_user
