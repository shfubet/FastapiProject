from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import select

from app.core.db import Session
from app.core.logger import logger
from app.models import User
from app.repositories.repository import Repository


class UserRepository(Repository[User, None, None]):
    Model = User

    @classmethod
    async def get_by_id(cls, db: Session, user_id: int) -> Optional[User]:
        """
        根据主键获取单个记录
        """
        logger.debug_with("CRUD: get user by id", "user_id", user_id)
        stmt = select(cls.Model).where(
            cls.Model.id == user_id,
            cls.Model.is_delete == False  # noqa: E712
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @classmethod
    async def get_by_email(cls, db: Session, email: str) -> Optional[User]:
        """
        根据邮箱获取用户
        """
        logger.debug_with("CRUD: get user by email", "email", email)
        stmt = select(cls.Model).where(
            cls.Model.email == email,
            cls.Model.is_delete == False  # noqa: E712
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()
