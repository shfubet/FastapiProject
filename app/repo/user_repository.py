from typing import Optional

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql.expression import select

from app.core.db import Session
from app.core.logger import logger
from app.model import User
from app.repo.repository import Repository
# from app.schemas.users import UserCreate


class UserRepository(Repository):
    Model = User


    @classmethod
    async def get(cls, db: Session, user_id: int) -> Optional[Model]:
        """
        根据主键获取单个记录
        """
        logger.debug_with("CRUD: 根据ID获取记录", "model", cls.Model)

        try:
            # 方法1: 使用 scalar_one_or_none()（推荐）
            result = await db.execute(select(cls.Model).where(cls.Model.id == user_id))
            return result.scalar_one_or_none()

            # 或者方法2: 如果你的数据库支持，直接使用 get
            # return await db.get(cls.Model, user_id)

        except Exception as e:
            logger.error(f"数据库查询错误: {e}")
            raise