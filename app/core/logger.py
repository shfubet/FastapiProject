import json
import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Dict, Any

from fastapi import FastAPI

from app.core import CONFIG

LOGFORMAT = "%(asctime)s - %(levelname)s - %(pathname)s:%(lineno)d - %(message)s"

LOG_LEVELS = ["INFO", "DEBUG", "WARNING", "ERROR", "CRITICAL"]


class LogConfig:
    """日志配置类"""

    def __init__(
            self,
            log_level: str = "INFO",
            log_dir: str = "logs",
            log_file: str = "app.log",
            output: str = "console",
            max_file_size: int = 10 * 1024 * 1024,  # 10MB
            backup_count: int = 5,
    ):
        if log_level.upper() not in LOG_LEVELS:
            raise RuntimeError(f"log_level:{log_level} is not supported.")
        self.log_level = getattr(logging, log_level.upper())
        self.log_dir = Path(log_dir)
        self.log_file = log_file
        self.max_file_size = max_file_size
        self.backup_count = backup_count
        self.enable_console = False
        self.enable_file = False
        if output == "console":
            self.enable_console = True
        elif output == "file":
            self.enable_file = True
        else:
            raise RuntimeError(f"output:{output} is not supported.")
        # 创建日志目录
        self.log_dir.mkdir(exist_ok=True)


class Logger:
    """日志管理器"""

    def __init__(self, config: LogConfig):
        self.config = config
        self.logger = logging.getLogger("APP")
        self.logger.setLevel(config.log_level)

        # 清除现有处理器
        self.logger.handlers.clear()

        self._setup_handlers()

    def setup_logging(
            self,
            app: FastAPI,
            log_level: str = "INFO",
            log_dir: str = "logs",
            log_file: str = "app.log",
            enable_middleware: bool = True
    ) -> None:
        """
         Args:
             app: FastAPI应用实例
             log_level: 日志级别
             log_dir: 日志目录
             log_file: 日志文件名
             enable_middleware: 是否启用HTTP请求日志中间件

         Returns:
             Logger: 日志管理器实例
         """
        pass

    # app.add_middleware(LoggingMiddleware, logger=logger)

    def _setup_handlers(self):
        """设置日志处理器"""

        # 控制台处理器
        if self.config.enable_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(self.config.log_level)
            console_handler.setFormatter(logging.Formatter(LOGFORMAT))
            self.logger.addHandler(console_handler)

        # 文件处理器
        if self.config.enable_file:
            file_handler = RotatingFileHandler(
                filename=self.config.log_dir.joinpath(self.config.log_file),
                maxBytes=self.config.max_file_size,
                backupCount=self.config.backup_count,
                encoding='utf-8'
            )
            file_handler.setLevel(self.config.log_level)
            file_handler.setFormatter(logging.Formatter(LOGFORMAT))
            self.logger.addHandler(file_handler)

    def get_logger(self):
        """获取日志器"""
        return self.logger

    def info(self, message: str):
        self.logger.info(message, stacklevel=2)

    def debug(self, message: str):
        self.logger.debug(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message)

    def debug_with(self, message: str, *args, **kwargs):
        self.get_message("debug", message, *args, **kwargs)

    def info_with(self, message, *args, **kwargs):
        self.get_message("info", message, *args, **kwargs)

    def warning_with(self, message, *args, **kwargs):
        self.get_message("warning", message, *args, **kwargs)

    def error_with(self, message, *args, **kwargs):
        self.get_message("error", message, *args, **kwargs)

    def get_message(self, level: str, message: str, *args, **kwargs) -> None:
        params: Dict[str, Any] = dict()
        for i in range(0, len(args), 2):
            if i == len(args) - 1:
                params[str(args[i])] = ""
            else:
                params[str(args[i])] = str(args[i + 1])
        params.update(kwargs)
        if params:
            getattr(self.logger, level)(message + ":" + json.dumps(params, ensure_ascii=False), stacklevel=3)
        else:
            getattr(self.logger, level)(message, stacklevel=3)


logger = Logger(LogConfig(CONFIG.logs.level, CONFIG.logs.logDir, CONFIG.logs.fileName, CONFIG.logs.output))

#
# class LoggingMiddleware(BaseHTTPMiddleware):
#     """HTTP请求日志中间件"""
#
#     def __init__(self, app, logger: Logger, log_requests: bool = True, log_responses: bool = True):
#         super().__init__(app)
#         self.logger = logger.get_logger()
#         self.log_requests = log_requests
#         self.log_responses = log_responses
#
#     async def dispatch(self, request: Request, call_next):
#         # 记录请求开始时间
#         start_time = time.time()
#
#         # 生成请求ID
#         request_id = f"{int(time.time() * 1000000)}"
#
#         # 记录请求信息
#         if self.log_requests:
#             request_data = {
#                 "request_id": request_id,
#                 "method": request.method,
#                 "url": str(request.url),
#                 "client_ip": request.client.host if request.client else None,
#                 "user_agent": request.headers.get("user-agent"),
#                 "headers": dict(request.headers)
#             }
#
#             # 记录请求体（对于POST/PUT请求）
#             if request.method in ["POST", "PUT", "PATCH"]:
#                 try:
#                     body = await request.body()
#                     if body:
#                         # 限制日志中body的长度
#                         body_str = body.decode('utf-8')[:1000]
#                         request_data["body"] = body_str
#                 except Exception as e:
#                     request_data["body_error"] = str(e)
#
#             self.logger.info("HTTP Request", extra={"extra_data": request_data})
#
#         # 处理请求
#         try:
#             response = await call_next(request)
#             process_time = time.time() - start_time
#
#             # 记录响应信息
#             if self.log_responses:
#                 response_data = {
#                     "request_id": request_id,
#                     "status_code": response.status_code,
#                     "process_time": round(process_time, 4),
#                     "response_headers": dict(response.headers)
#                 }
#
#                 log_level = "error" if response.status_code >= 400 else "info"
#                 getattr(self.logger, log_level)("HTTP Response", extra={"extra_data": response_data})
#
#             return response
#
#         except Exception as e:
#             process_time = time.time() - start_time
#
#             # 记录异常
#             error_data = {
#                 "request_id": request_id,
#                 "error": str(e),
#                 "error_type": type(e).__name__,
#                 "process_time": round(process_time, 4),
#                 "traceback": traceback.format_exc()
#             }
#
#             self.logger.error("HTTP Request Error", extra={"extra_data": error_data})
#             raise
