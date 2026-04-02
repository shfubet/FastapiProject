import logging

from pydantic import BaseModel, Field


class LogsConfig(BaseModel):
    level: str
    output: str
    logDir: str
    fileName: str


class ServiceConfig(BaseModel):
    port: int


class MysqlConfig(BaseModel):
    url: str
    poolSize: int
    poolTimeout: int
    autocommit: bool


class RedisConfig(BaseModel):
    host: str
    port: int
    password: str


class AppConfig(BaseModel):
    service: ServiceConfig
    mysql: MysqlConfig
    redis: RedisConfig
    logs: LogsConfig
