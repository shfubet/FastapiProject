from app.core.response import ResponseCode


class BusinessException(Exception):
    """业务异常"""

    def __init__(self, message: str, code: int = ResponseCode.INTERNAL_ERROR.value):
        self.message = message
        self.code = code
        super().__init__(self.message)


class NotFoundException(BusinessException):
    """资源不存在异常"""

    def __init__(self, message: str = "资源不存在"):
        super().__init__(message, ResponseCode.NOT_FOUND.value)


class BadRequestException(BusinessException):
    """请求参数错误异常"""

    def __init__(self, message: str = "请求参数错误"):
        super().__init__(message, ResponseCode.BAD_REQUEST.value)


class UnauthorizedException(BusinessException):
    """未授权异常"""

    def __init__(self, message: str = "未授权访问"):
        super().__init__(message, ResponseCode.UNAUTHORIZED.value)
