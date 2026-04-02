from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import db_session


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    数据库会话依赖注入
    """
    async with db_session() as session:
        try:
            yield session
        finally:
            await session.close()
