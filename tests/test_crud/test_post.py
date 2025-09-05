from sqlalchemy.orm import Session

from app.models.post import Post
from app.schemas.post import PostUpdate, PostCreate
from app.schemas.tag import TagCreate
from tests.conftest import db_session, test_user, test_post
from app.crud.post import get_post_by_id, get_posts_by_category, update_post, delete_post, create_post


def test_create_post(db_session: Session, test_post, test_user):
    posts_in_db = db_session.query(Post).all()

    assert len(posts_in_db) == 1
    assert posts_in_db[0].title == test_post.title


def test_create_post_with_tags(db_session: Session, test_user):
    post_data = PostCreate(
        title='TestPost',
        content='TestContent',
        category='TestCategory',
        is_pinned=True,
        tags=[TagCreate(name='TestTag')]
    )
    post = create_post(db_session, post_data, test_user.id)

    assert post.title == 'TestPost'
    assert len(post.tags) == 1
    assert post.tags[0].name == 'TestTag'


def test_get_post_by_id(db_session: Session, test_post):
    post = get_post_by_id(db_session,test_post.id)

    assert post.id == test_post.id
    assert post.title == test_post.title


def test_get_posts_by_category(db_session: Session, test_post):
    post = get_posts_by_category(db_session,test_post.category)

    assert post[0].id == test_post.id
    assert post[0].category == test_post.category


def test_update_post(db_session: Session, test_post, test_user):
    update_data = PostUpdate(title='updated', tags=[TagCreate(name='test')])
    post = update_post(db_session,test_post,update_data)

    assert post.title == 'updated'
    assert post.tags[0].name == 'test'


def test_delete_post(db_session: Session, test_post):
    deleted = delete_post(db_session, test_post.id)

    assert get_post_by_id(db_session,test_post.id) is None
    assert deleted == 1





