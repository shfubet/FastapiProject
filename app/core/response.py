from pydantic.generics import GenericModel

from typing import Any, Optional, Generic, TypeVar, Mapping
from starlette.responses import JSONResponse
from starlette.background import BackgroundTask
from enum import Enum

T = TypeVar('T')


class ResponseCode(Enum):
    """响应状态码枚举"""
    SUCCESS = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    INTERNAL_ERROR = 500


class JsonResponse(JSONResponse):
    def __init__(self,
                 data: Optional[dict] = None,
                 code: int = 0,
                 message: str = "OK",
                 status_code: int = 200,
                 headers: Mapping[str, str] | None = None,
                 media_type: str | None = None,
                 background: BackgroundTask | None = None) -> None:
        if not data:
            data = {}
        content = {
            "code": code,
            "message": message,
            "data": data
        }
        super().__init__(content, status_code, headers, media_type, background)
