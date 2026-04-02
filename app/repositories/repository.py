from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from sqlalchemy import select, func, or_, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.model import BaseModel
from app.core.logger import logger

ModelType = TypeVar("ModelType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound="BaseModel")
UpdateSchemaType = TypeVar("UpdateSchemaType", bound="BaseModel")


class Repository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    通用数据库操作基类（异步）

    提供标准的数据库操作方法，所有具体的数据库操作类都应该继承这个基类
    """
    Model: Type[ModelType]

    @classmethod
    async def get(cls, db: AsyncSession, id: int) -> Optional[ModelType]:
        """
        根据主键获取单个记录

        Args:
            db: 数据库会话
            id: 主键值

        Returns:
            模型实例或 None
        """
        logger.debug_with("CRUD: get by id", "model", cls.Model.__name__, "id", id)
        stmt = select(cls.Model).where(
            cls.Model.id == id,
            cls.Model.is_delete == False  # noqa: E712
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @classmethod
    async def get_multi(
        cls,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100,
        order_by: str = "id",
        order_desc: bool = True
    ) -> tuple[List[ModelType], int]:
        """
        获取多个记录（分页）

        Args:
            db: 数据库会话
            skip: 跳过的记录数
            limit: 返回的最大记录数
            order_by: 排序字段
            order_desc: 是否降序排列

        Returns:
            (记录列表, 总记录数)
        """
        logger.debug_with(
            "CRUD: get multiple",
            "model", cls.Model.__name__,
            "skip", skip,
            "limit", limit,
            "order_by", order_by
        )

        # 获取总数
        count_stmt = select(func.count(cls.Model.id)).where(cls.Model.is_delete == False)  # noqa: E712
        total_result = await db.execute(count_stmt)
        total = total_result.scalar()

        # 构建排序
        order_column = getattr(cls.Model, order_by, cls.Model.id)
        order_func = desc if order_desc else asc

        # 获取记录
        stmt = (
            select(cls.Model)
            .where(cls.Model.is_delete == False)  # noqa: E712
            .offset(skip)
            .limit(limit)
            .order_by(order_func(order_column))
        )
        result = await db.execute(stmt)
        items = result.scalars().all()

        logger.debug_with("CRUD: get multiple done", "total", total, "returned", len(items))
        return list(items), total

    @classmethod
    async def create(cls, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        """
        创建新记录

        Args:
            db: 数据库会话
            obj_in: 创建数据的 Pydantic 模型

        Returns:
            创建的模型实例
        """
        logger.debug_with("CRUD: create", "model", cls.Model.__name__)

        try:
            obj_in_data = obj_in.model_dump() if hasattr(obj_in, 'model_dump') else obj_in.dict()
            db_obj = cls.Model(**obj_in_data)
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)

            logger.debug_with("CRUD: created", "model", cls.Model.__name__, "id", db_obj.id)
            return db_obj

        except Exception as e:
            logger.error_with("CRUD: create failed", "model", cls.Model.__name__, "error", str(e))
            await db.rollback()
            raise

    @classmethod
    async def update(
        cls,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """
        更新记录

        Args:
            db: 数据库会话
            db_obj: 要更新的数据库对象
            obj_in: 更新数据（Pydantic 模型或字典）

        Returns:
            更新后的模型实例
        """
        logger.debug_with("CRUD: update", "model", cls.Model.__name__, "id", db_obj.id)

        try:
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.model_dump(exclude_unset=True) if hasattr(obj_in, 'model_dump') else obj_in.dict(exclude_unset=True)

            for field, value in update_data.items():
                if hasattr(db_obj, field):
                    setattr(db_obj, field, value)

            await db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)

            logger.debug_with("CRUD: updated", "model", cls.Model.__name__, "id", db_obj.id)
            return db_obj

        except Exception as e:
            logger.error_with("CRUD: update failed", "model", cls.Model.__name__, "id", db_obj.id, "error", str(e))
            await db.rollback()
            raise

    @classmethod
    async def delete(cls, db: AsyncSession, *, id: int) -> Optional[ModelType]:
        """
        软删除记录 (is_delete=True)

        Args:
            db: 数据库会话
            id: 要删除的记录ID

        Returns:
            被删除的模型实例或 None
        """
        logger.debug_with("CRUD: soft delete", "model", cls.Model.__name__, "id", id)

        try:
            stmt = select(cls.Model).where(
                cls.Model.id == id,
                cls.Model.is_delete == False  # noqa: E712
            )
            result = await db.execute(stmt)
            obj = result.scalar_one_or_none()

            if obj:
                obj.is_delete = True
                await db.commit()
                await db.refresh(obj)
                logger.debug_with("CRUD: soft deleted", "model", cls.Model.__name__, "id", id)
            else:
                logger.warning_with("CRUD: record not found for delete", "model", cls.Model.__name__, "id", id)

            return obj

        except Exception as e:
            logger.error_with("CRUD: delete failed", "model", cls.Model.__name__, "id", id, "error", str(e))
            await db.rollback()
            raise

    @classmethod
    async def search(
        cls,
        db: AsyncSession,
        *,
        search_fields: List[str],
        search_term: str,
        skip: int = 0,
        limit: int = 100
    ) -> tuple[List[ModelType], int]:
        """
        多字段搜索

        Args:
            db: 数据库会话
            search_fields: 要搜索的字段列表
            search_term: 搜索关键词
            skip: 跳过的记录数
            limit: 返回的最大记录数

        Returns:
            (搜索结果列表, 总记录数)
        """
        logger.debug_with(
            "CRUD: search",
            "model", cls.Model.__name__,
            "fields", search_fields,
            "term", search_term
        )

        search_conditions = []
        for field_name in search_fields:
            if hasattr(cls.Model, field_name):
                field = getattr(cls.Model, field_name)
                try:
                    search_conditions.append(field.contains(search_term))
                except Exception:
                    search_conditions.append(field == search_term)

        if not search_conditions:
            logger.warning_with("CRUD: no valid search fields", "model", cls.Model.__name__)
            return [], 0

        search_condition = or_(*search_conditions)
        base_condition = cls.Model.is_delete == False  # noqa: E712

        # 获取总数
        count_stmt = select(func.count(cls.Model.id)).where(base_condition, search_condition)
        total_result = await db.execute(count_stmt)
        total = total_result.scalar()

        # 获取记录
        stmt = (
            select(cls.Model)
            .where(base_condition, search_condition)
            .offset(skip)
            .limit(limit)
            .order_by(desc(cls.Model.id))
        )
        result = await db.execute(stmt)
        items = result.scalars().all()

        logger.debug_with("CRUD: search done", "total", total, "returned", len(items))
        return list(items), total

    @classmethod
    async def get_by_field(
        cls,
        db: AsyncSession,
        field_name: str,
        field_value: Any
    ) -> Optional[ModelType]:
        """
        根据指定字段获取记录

        Args:
            db: 数据库会话
            field_name: 字段名
            field_value: 字段值

        Returns:
            模型实例或 None
        """
        if not hasattr(cls.Model, field_name):
            raise ValueError(f"模型 {cls.Model.__name__} 没有字段 {field_name}")

        logger.debug_with(
            "CRUD: get by field",
            "model", cls.Model.__name__,
            "field", field_name,
            "value", field_value
        )

        field = getattr(cls.Model, field_name)
        stmt = select(cls.Model).where(
            field == field_value,
            cls.Model.is_delete == False  # noqa: E712
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()
