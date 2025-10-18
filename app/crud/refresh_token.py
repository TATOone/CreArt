from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.refresh_token import RefreshToken


async def create_refresh_token_in_db(db: AsyncSession, refresh_token: str, user_id: int) -> RefreshToken:
    new_refresh_token = RefreshToken(user_id=user_id, refresh_token=refresh_token)
    db.add(new_refresh_token)
    await db.commit()
    await db.refresh(new_refresh_token)
    return new_refresh_token


async def delete_refresh_token(db: AsyncSession, refresh_token: str) -> bool | None:
    result = await db.execute(select(RefreshToken).where(RefreshToken.refresh_token == refresh_token))
    token = result.scalars().first()
    if not token:
        return None
    await db.delete(token)
    await db.commit()
    return True


async def get_refresh_token(db: AsyncSession, refresh_token: str) -> RefreshToken | None:
    result = await db.execute(select(RefreshToken).where(RefreshToken.refresh_token == refresh_token))
    token = result.scalars().first()
    if not token:
        return None
    return token