from functools import wraps
from typing import List, Callable, Type, Any
from pydantic import BaseModel
import asyncio


def route(path: str, methods: List[str], response_model: Type[BaseModel] = None, *args, **kwargs) -> Callable:
    def decorator(func: Callable):
        if asyncio.iscoroutinefunction(func):
            # 如果是异步函数，保持异步
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                return await func(*args, **kwargs)

            async_wrapper._route_info = {
                "path": path,
                "methods": methods,
                "response_model": response_model,
                "args": args,
                "kwargs": kwargs,
            }
            return async_wrapper
        else:
            # 如果是同步函数，保持同步
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            sync_wrapper._route_info = {
                "path": path,
                "methods": methods,
                "response_model": response_model,
                "args": args,
                "kwargs": kwargs,
            }
            return sync_wrapper

    return decorator