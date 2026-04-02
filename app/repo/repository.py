from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from sqlalchemy.orm import Session
from sqlalchemy import select, func, or_, and_, desc, asc
from pydantic import BaseModel
from app.core.model import BaseModel as Model
from app.core.logger import logger

CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class Repository(Generic[CreateSchemaType, UpdateSchemaType]):
    """
    通用 数据库操作 基类

    提供标准的数据库操作方法，所有具体的 数据库操作 类都应该继承这个基类
    """
    Model: Type[Model]

    @classmethod
    async def get(cls, db: Session, user_id: int) -> Optional[Model]:
        """
        根据主键获取单个记录

        Args:
            db: 数据库会话
            user_id: 主键值

        Returns:
            模型实例或 None
        """

        logger.debug_with("CRUD: 根据ID获取记录", "model", cls.Model)
        result =  await db.execute(select(cls.Model).where(cls.Model.id == user_id))

        return result.scalars().first()
    #
    # def get_multi(
    #         self,
    #         db: Session,
    #         *,
    #         skip: int = 0,
    #         limit: int = 100,
    #         order_by: str = "id",
    #         order_desc: bool = True
    # ) -> tuple[List[ModelType], int]:
    #     """
    #     获取多个记录（分页）
    #
    #     Args:
    #         db: 数据库会话
    #         skip: 跳过的记录数
    #         limit: 返回的最大记录数
    #         order_by: 排序字段
    #         order_desc: 是否降序排列
    #
    #     Returns:
    #         (记录列表, 总记录数)
    #     """
    #     logger.debug_with("CRUD: 获取记录列表",
    #                       "model", self.model.__name__,
    #                       "skip", skip,
    #                       "limit", limit,
    #                       "order_by", order_by)
    #
    #     # 获取总数
    #     count_stmt = select(func.count(self.model.id))
    #     total = db.execute(count_stmt).scalar()
    #
    #     # 构建排序
    #     order_column = getattr(self.model, order_by, self.model.id)
    #     order_func = desc if order_desc else asc
    #
    #     # 获取记录
    #     stmt = select(self.model).offset(skip).limit(limit).order_by(order_func(order_column))
    #     items = db.execute(stmt).scalars().all()
    #
    #     logger.debug_with("CRUD: 记录获取完成", "total", total, "returned", len(items))
    #     return list(items), total
    #
    # def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
    #     """
    #     创建新记录
    #
    #     Args:
    #         db: 数据库会话
    #         obj_in: 创建数据的 Pydantic 模型
    #
    #     Returns:
    #         创建的模型实例
    #     """
    #     logger.debug_with("CRUD: 创建记录", "model", self.model.__name__)
    #
    #     try:
    #         # 将 Pydantic 模型转换为字典
    #         obj_in_data = obj_in.model_dump()
    #
    #         # 创建数据库模型实例
    #         db_obj = self.model(**obj_in_data)
    #
    #         # 保存到数据库
    #         db.add(db_obj)
    #         db.commit()
    #         db.refresh(db_obj)
    #
    #         logger.debug_with("CRUD: 记录创建成功", "model", self.model.__name__, "id", db_obj.id)
    #         return db_obj
    #
    #     except Exception as e:
    #         logger.error_with("CRUD: 记录创建失败", "model", self.model.__name__, "error", str(e))
    #         db.rollback()
    #         raise
    #
    # def update(
    #         self,
    #         db: Session,
    #         *,
    #         db_obj: ModelType,
    #         obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    # ) -> ModelType:
    #     """
    #     更新记录
    #
    #     Args:
    #         db: 数据库会话
    #         db_obj: 要更新的数据库对象
    #         obj_in: 更新数据（Pydantic 模型或字典）
    #
    #     Returns:
    #         更新后的模型实例
    #     """
    #     logger.debug_with("CRUD: 更新记录", "model", self.model.__name__, "id", db_obj.id)
    #
    #     try:
    #         # 处理输入数据
    #         if isinstance(obj_in, dict):
    #             update_data = obj_in
    #         else:
    #             update_data = obj_in.model_dump(exclude_unset=True)
    #
    #         # 更新字段
    #         for field, value in update_data.items():
    #             if hasattr(db_obj, field):
    #                 setattr(db_obj, field, value)
    #
    #         # 保存更改
    #         db.add(db_obj)
    #         db.commit()
    #         db.refresh(db_obj)
    #
    #         logger.debug_with("CRUD: 记录更新成功", "model", self.model.__name__, "id", db_obj.id)
    #         return db_obj
    #
    #     except Exception as e:
    #         logger.error_with("CRUD: 记录更新失败", "model", self.model.__name__, "id", db_obj.id, "error", str(e))
    #         db.rollback()
    #         raise
    #
    # def delete(self, db: Session, *, id: int) -> Optional[ModelType]:
    #     """
    #     删除记录
    #
    #     Args:
    #         db: 数据库会话
    #         id: 要删除的记录ID
    #
    #     Returns:
    #         被删除的模型实例或 None
    #     """
    #     logger.debug_with("CRUD: 删除记录", "model", self.model.__name__, "id", id)
    #
    #     try:
    #         obj = db.get(self.model, id)
    #         if obj:
    #             db.delete(obj)
    #             db.commit()
    #             logger.debug_with("CRUD: 记录删除成功", "model", self.model.__name__, "id", id)
    #         else:
    #             logger.warning_with("CRUD: 要删除的记录不存在", "model", self.model.__name__, "id", id)
    #         return obj
    #
    #     except Exception as e:
    #         logger.error_with("CRUD: 记录删除失败", "model", self.model.__name__, "id", id, "error", str(e))
    #         db.rollback()
    #         raise
    #
    # def get_by_field(
    #         self,
    #         db: Session,
    #         field_name: str,
    #         field_value: Any
    # ) -> Optional[ModelType]:
    #     """
    #     根据指定字段获取记录
    #
    #     Args:
    #         db: 数据库会话
    #         field_name: 字段名
    #         field_value: 字段值
    #
    #     Returns:
    #         模型实例或 None
    #     """
    #     if not hasattr(self.model, field_name):
    #         raise ValueError(f"模型 {self.model.__name__} 没有字段 {field_name}")
    #
    #     logger.debug_with("CRUD: 根据字段获取记录",
    #                       "model", self.model.__name__,
    #                       "field", field_name,
    #                       "value", field_value)
    #
    #     field = getattr(self.model, field_name)
    #     stmt = select(self.model).where(field == field_value)
    #     return db.execute(stmt).scalar_one_or_none()
    #
    # def get_multi_by_field(
    #         self,
    #         db: Session,
    #         field_name: str,
    #         field_value: Any,
    #         *,
    #         skip: int = 0,
    #         limit: int = 100
    # ) -> tuple[List[ModelType], int]:
    #     """
    #     根据指定字段获取多个记录
    #
    #     Args:
    #         db: 数据库会话
    #         field_name: 字段名
    #         field_value: 字段值
    #         skip: 跳过的记录数
    #         limit: 返回的最大记录数
    #
    #     Returns:
    #         (记录列表, 总记录数)
    #     """
    #     if not hasattr(self.model, field_name):
    #         raise ValueError(f"模型 {self.model.__name__} 没有字段 {field_name}")
    #
    #     field = getattr(self.model, field_name)
    #     condition = field == field_value
    #
    #     # 获取总数
    #     count_stmt = select(func.count(self.model.id)).where(condition)
    #     total = db.execute(count_stmt).scalar()
    #
    #     # 获取记录
    #     stmt = select(self.model).where(condition).offset(skip).limit(limit)
    #     items = db.execute(stmt).scalars().all()
    #
    #     return list(items), total
    #
    # def search(
    #         self,
    #         db: Session,
    #         *,
    #         search_fields: List[str],
    #         search_term: str,
    #         skip: int = 0,
    #         limit: int = 100
    # ) -> tuple[List[ModelType], int]:
    #     """
    #     多字段搜索
    #
    #     Args:
    #         db: 数据库会话
    #         search_fields: 要搜索的字段列表
    #         search_term: 搜索关键词
    #         skip: 跳过的记录数
    #         limit: 返回的最大记录数
    #
    #     Returns:
    #         (搜索结果列表, 总记录数)
    #     """
    #     logger.debug_with("CRUD: 多字段搜索",
    #                       "model", self.model.__name__,
    #                       "fields", search_fields,
    #                       "term", search_term)
    #
    #     # 构建搜索条件
    #     search_conditions = []
    #     for field_name in search_fields:
    #         if hasattr(self.model, field_name):
    #             field = getattr(self.model, field_name)
    #             # 检查字段是否支持 contains 操作（字符串字段）
    #             try:
    #                 search_conditions.append(field.contains(search_term))
    #             except Exception:
    #                 # 如果字段不支持 contains，尝试精确匹配
    #                 search_conditions.append(field == search_term)
    #
    #     if not search_conditions:
    #         logger.warning_with("CRUD: 没有有效的搜索字段", "model", self.model.__name__)
    #         return [], 0
    #
    #     # 组合搜索条件（OR 关系）
    #     search_condition = or_(*search_conditions)
    #
    #     # 获取总数
    #     count_stmt = select(func.count(self.model.id)).where(search_condition)
    #     total = db.execute(count_stmt).scalar()
    #
    #     # 获取记录
    #     stmt = (
    #         select(self.model)
    #         .where(search_condition)
    #         .offset(skip)
    #         .limit(limit)
    #         .order_by(self.model.id.desc())
    #     )
    #     items = db.execute(stmt).scalars().all()
    #
    #     logger.debug_with("CRUD: 搜索完成", "total", total, "returned", len(items))
    #     return list(items), total
    #
    # def bulk_create(self, db: Session, *, obj_in_list: List[CreateSchemaType]) -> List[ModelType]:
    #     """
    #     批量创建记录
    #
    #     Args:
    #         db: 数据库会话
    #         obj_in_list: 创建数据列表
    #
    #     Returns:
    #         创建的模型实例列表
    #     """
    #     logger.debug_with("CRUD: 批量创建记录", "model", self.model.__name__, "count", len(obj_in_list))
    #
    #     try:
    #         db_objs = []
    #         for obj_in in obj_in_list:
    #             obj_in_data = obj_in.model_dump()
    #             db_obj = self.model(**obj_in_data)
    #             db_objs.append(db_obj)
    #
    #         db.add_all(db_objs)
    #         db.commit()
    #
    #         for db_obj in db_objs:
    #             db.refresh(db_obj)
    #
    #         logger.debug_with("CRUD: 批量创建成功", "model", self.model.__name__, "count", len(db_objs))
    #         return db_objs
    #
    #     except Exception as e:
    #         logger.error_with("CRUD: 批量创建失败", "model", self.model.__name__, "error", str(e))
    #         db.rollback()
    #         raise
    #
    # def bulk_delete(self, db: Session, *, ids: List[int]) -> int:
    #     """
    #     批量删除记录
    #
    #     Args:
    #         db: 数据库会话
    #         ids: 要删除的ID列表
    #
    #     Returns:
    #         删除的记录数
    #     """
    #     logger.debug_with("CRUD: 批量删除记录", "model", self.model.__name__, "ids", ids)
    #
    #     try:
    #         stmt = select(self.model).where(self.model.id.in_(ids))
    #         objs = db.execute(stmt).scalars().all()
    #
    #         count = len(objs)
    #         for obj in objs:
    #             db.delete(obj)
    #
    #         db.commit()
    #
    #         logger.debug_with("CRUD: 批量删除成功", "model", self.model.__name__, "count", count)
    #         return count
    #
    #     except Exception as e:
    #         logger.error_with("CRUD: 批量删除失败", "model", self.model.__name__, "error", str(e))
    #         db.rollback()
    #         raise
    #
    # def exists(self, db: Session, *, id: int) -> bool:
    #     """
    #     检查记录是否存在
    #
    #     Args:
    #         db: 数据库会话
    #         id: 记录ID
    #
    #     Returns:
    #         是否存在
    #     """
    #     stmt = select(func.count(self.model.id)).where(self.model.id == id)
    #     count = db.execute(stmt).scalar()
    #     return count > 0
    #
    # def count(self, db: Session) -> int:
    #     """
    #     获取表中记录总数
    #
    #     Args:
    #         db: 数据库会话
    #
    #     Returns:
    #         记录总数
    #     """
    #     stmt = select(func.count(self.model.id))
    #     return db.execute(stmt).scalar()
