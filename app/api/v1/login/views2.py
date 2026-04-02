from typing import Annotated, Any

from fastapi import APIRouter, Depends
from fastapi import FastAPI, Path, Query
from pydantic import BaseModel

from app.core.view import MethodView
from app.core.db import Session
from app.core.decorator import route
from app.core.exceptions import NotFoundException
# from app.api import CustomRoute
from app.core.logger import logger
from app.core.response import JSONResponse
from app.main import app
from app.model import User
from app.repo.user_repository import UserRepository
from app.schemas.users import UserDetail

LoginRouter = APIRouter(prefix="/users", tags=["login"], )


class UserView(MethodView):
    router_prefix = "/users"
    repo_class = UserRepository
    response_schema = UserDetail

    @app.get("/{item_id}")
    async def getUser(self, item_id: int, db: Session) :
        """获取详情"""
        try:
            logger.info_with("获取详情", "item_id", item_id)

            item = await self.repo_class.get(db, user_id=item_id)
            if not item:
                raise NotFoundException(f"ID为{item_id}的记录不存在")

            # 详细调试信息
            print(f"Item type: {type(item)}")
            print(f"Item value: {item}")
            print(f"Item __dict__: {getattr(item, '__dict__', 'No __dict__')}")
            print(f"Response schema: {self.response_schema}")
            #
            # # 尝试不同的验证方式
            # try:
            #     validated_item = self.response_schema.model_validate(item)
            #     print(f"Validation successful: {validated_item}")
            # except Exception as ve:
            #     print(f"Direct validation failed: {ve}")
            #     # 尝试转换为字典
            #     if hasattr(item, '__dict__'):
            #         item_dict = {k: v for k, v in item.__dict__.items() if not k.startswith('_')}
            #         validated_item = self.response_schema.model_validate(item_dict)
            #     else:
            #         raise ve

            return self.response_schema.model_validate(item)

        except Exception as e:
            logger.error(f"获取详情失败: {type(e).__name__}: {e}")
            return self.handle_exception(e)
