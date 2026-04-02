from abc import ABC, abstractmethod, ABCMeta
from typing import Type, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from app.core.db import get_db, Session
from app.core.response import  JsonResponse
from app.core.exceptions import BusinessException, NotFoundException, BadRequestException
from app.core.logger import logger
from app.schemas.users import UserDetail


class BaseView(metaclass=ABCMeta):
    """基础视图类"""

    # 子类需要定义的属性
    router_prefix: str = ""
    router_tags: list = []
    # 数据模型相关
    repo_class: Type = None
    service_class: Type = None
    create_schema: Type[BaseModel] = None
    update_schema: Type[BaseModel] = None
    response_schema: Type[BaseModel] = None

    def __new__(cls, *args, **kwargs):
        c = super().__new__(cls, *args, **kwargs)
        c.router = APIRouter(prefix=cls.router_prefix, tags=cls.router_tags)
        c._register_routes()
        return c

    def _register_routes(self):
        for attr_name in dir(self):
            func = getattr(self, attr_name)
            if callable(func) and hasattr(func, "_route_info"):
                info = func._route_info
                path = info["path"]
                methods = info["methods"]
                schema = info["response_model"] or self.response_schema  # 使用类的 response_schema 作为默认值
                args = info["args"]
                kwargs = info["kwargs"]

                if schema:
                    # 检查是否已经是 BaseResponse 类型
                    if hasattr(schema, '__origin__') and schema.__origin__ is JsonResponse:
                        response_model = schema
                    else:
                        # 包装为 BaseResponse
                        class Wrapped():  # type: ignore
                            pass

                        response_model = Wrapped
                else:
                    response_model = None

                self.router.add_api_route(
                    path,
                    func,
                    methods=methods,
                    response_model=response_model,
                    *args,
                    **kwargs,
                )

    def handle_exception(self, e: Exception) -> JsonResponse:
        """统一异常处理"""
        if isinstance(e, BusinessException):
            logger.warning_with("业务异常", "message", e.message, "code", e.code)
            return JsonResponse(message=e.message, code=e.code)
        else:
            logger.error_with("系统异常", "error", str(e), "type", type(e).__name__)
            return JsonResponse(message="系统内部错误")


class MethodView(BaseView):
    """通用视图类"""
    pass
#
#     async def get(self, id: int, db: Session) -> BaseResponse:
#         """获取详情"""
#         try:
#             logger.info_with("获取详情", "item_id", id)
#
#             item = await self.crud_class.get(db, user_id=id)
#             if not item:
#                 raise NotFoundException(f"ID为{item_id}的记录不存在")
#
#             return BaseResponse.success(self.response_schema.model_validate(item), message="获取详情成功")
#
#         except Exception as e:
#             return self.handle_exception(e)

    # def query(
    #         self,
    #         db: Session = Depends(get_db),
    #         page: int = Query(1, ge=1, description="页码"),
    #         size: int = Query(10, ge=1, le=100, description="每页数量"),
    #         keyword: Optional[str] = Query(None, description="搜索关键词")
    # ) -> ListResponse:
    #     """获取列表数据"""
    #     try:
    #         logger.info_with("获取列表", "page", page, "size", size, "keyword", keyword)
    #
    #         skip = (page - 1) * size
    #         items, total = self.crud_class.query(db, skip=skip, limit=size, keyword=keyword)
    #
    #         pages = (total + size - 1) // size  # 向上取整
    #
    #         pagination_data = PaginationData(
    #             items=items,
    #             total=total,
    #             page=page,
    #             size=len(items),
    #             pages=pages
    #         )
    #
    #         return ListResponse.success(data=pagination_data, message="获取列表成功")
    #
    #     except Exception as e:
    #         return self.handle_exception(e)

    # def post(self, item_in: Any, db: Session) -> BaseResponse:
    #     """创建记录"""
    #     try:
    #         logger.info_with("创建记录", "data", str(item_in))
    #
    #         item = self.crud_class.create(db, obj_in=item_in)
    #
    #         return BaseResponse.created(data=item, message="创建成功")
    #
    #     except Exception as e:
    #         return self.handle_exception(e)
    #
    # def put(self, item_id: int, item_in: Any, db: Session = Depends(get_db)) -> BaseResponse:
    #     """完整更新记录"""
    #     try:
    #         logger.info_with("更新记录", "item_id", item_id, "data", str(item_in))
    #
    #         db_item = self.crud_class.get(db, id=item_id)
    #         if not db_item:
    #             raise NotFoundException(f"ID为{item_id}的记录不存在")
    #
    #         item = self.crud_class.update(db, db_obj=db_item, obj_in=item_in)
    #
    #         return BaseResponse.success(data=item, message="更新成功")
    #
    #     except Exception as e:
    #         return self.handle_exception(e)
    #
    # def patch(self, item_id: int, item_in: Any, db: Session = Depends(get_db)) -> BaseResponse:
    #     """部分更新记录"""
    #     try:
    #         logger.info_with("部分更新记录", "item_id", item_id, "data", str(item_in))
    #
    #         db_item = self.crud_class.get(db, id=item_id)
    #         if not db_item:
    #             raise NotFoundException(f"ID为{item_id}的记录不存在")
    #
    #         item = self.crud_class.update(db, db_obj=db_item, obj_in=item_in)
    #
    #         return BaseResponse.success(data=item, message="部分更新成功")
    #
    #     except Exception as e:
    #         return self.handle_exception(e)
    #
    # def delete(self, item_id: int, db: Session = Depends(get_db)) -> BaseResponse:
    #     """删除记录"""
    #     try:
    #         logger.info_with("删除记录", "item_id", item_id)
    #
    #         item = self.crud_class.delete(db, id=item_id)
    #         if not item:
    #             raise NotFoundException(f"ID为{item_id}的记录不存在")
    #
    #         return BaseResponse.success(data=item, message="删除成功")
    #
    #     except Exception as e:
    #         return self.handle_exception(e)
