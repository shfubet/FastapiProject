from typing import Optional, List, Tuple

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Session
from app.core.logger import logger
from app.models import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate, UserDetail, UserList


class UserService:
    """用户服务层"""

    @staticmethod
    async def get_user_by_id(db: Session, user_id: int) -> Optional[UserDetail]:
        """
        根据ID获取用户详情
        """
        logger.debug_with("Service: get user by id", "user_id", user_id)
        user = await UserRepository.get_by_id(db, user_id)
        if user:
            return UserDetail.model_validate(user)
        return None

    @staticmethod
    async def get_user_by_email(db: Session, email: str) -> Optional[UserDetail]:
        """
        根据邮箱获取用户详情
        """
        logger.debug_with("Service: get user by email", "email", email)
        user = await UserRepository.get_by_email(db, email)
        if user:
            return UserDetail.model_validate(user)
        return None

    @staticmethod
    async def get_users(
        db: Session,
        skip: int = 0,
        limit: int = 100
    ) -> Tuple[List[UserList], int]:
        """
        获取用户列表（分页）
        """
        logger.debug_with("Service: get users", "skip", skip, "limit", limit)
        users, total = await UserRepository.get_multi(db, skip=skip, limit=limit)
        items = [UserList.model_validate(u) for u in users]
        return items, total

    @staticmethod
    async def create_user(db: Session, user_in: UserCreate) -> UserDetail:
        """
        创建用户
        """
        logger.debug_with("Service: create user", "email", user_in.email)

        # 检查邮箱是否已存在
        existing = await UserRepository.get_by_email(db, user_in.email)
        if existing:
            raise ValueError(f"邮箱 {user_in.email} 已存在")

        user = await UserRepository.create(db, obj_in=user_in)
        return UserDetail.model_validate(user)

    @staticmethod
    async def update_user(
        db: Session,
        user_id: int,
        user_in: UserUpdate
    ) -> Optional[UserDetail]:
        """
        更新用户
        """
        logger.debug_with("Service: update user", "user_id", user_id)

        user = await UserRepository.get_by_id(db, user_id)
        if not user:
            return None

        # 检查邮箱是否被其他用户使用
        if user_in.email and user_in.email != user.email:
            existing = await UserRepository.get_by_email(db, user_in.email)
            if existing:
                raise ValueError(f"邮箱 {user_in.email} 已被使用")

        updated_user = await UserRepository.update(db, db_obj=user, obj_in=user_in)
        return UserDetail.model_validate(updated_user)

    @staticmethod
    async def delete_user(db: Session, user_id: int) -> bool:
        """
        删除用户（软删除）
        """
        logger.debug_with("Service: delete user", "user_id", user_id)
        user = await UserRepository.delete(db, id=user_id)
        return user is not None

    @staticmethod
    async def search_users(
        db: Session,
        keyword: str,
        skip: int = 0,
        limit: int = 100
    ) -> Tuple[List[UserList], int]:
        """
        搜索用户
        """
        logger.debug_with("Service: search users", "keyword", keyword)
        users, total = await UserRepository.search(
            db,
            search_fields=["name", "email"],
            search_term=keyword,
            skip=skip,
            limit=limit
        )
        items = [UserList.model_validate(u) for u in users]
        return items, total
