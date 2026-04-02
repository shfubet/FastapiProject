import sys
from typing import Any, AsyncGenerator, Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from app.core import CONFIG
from app.core.logger import logger


def create_engine_and_session() -> tuple[AsyncEngine, async_sessionmaker[AsyncSession]]:
    try:
        e = create_async_engine(
            CONFIG.mysql.url,
            echo=True,
            pool_size=CONFIG.mysql.poolSize,
            max_overflow=20,
            pool_timeout=CONFIG.mysql.poolTimeout,
            pool_pre_ping=True
        )
    except Exception as err:
        logger.error_with(f"failed to create database engine.", "error", err)
        sys.exit(1)
    s = async_sessionmaker(
        bind=e,
        class_=AsyncSession,
        autoflush=False,
        autocommit=CONFIG.mysql.autocommit,
        expire_on_commit=False
    )
    return e, s


db_engine, db_session = create_engine_and_session()


async def get_db() -> AsyncGenerator[AsyncSession | Any, Any]:
    async with db_session() as session:
        yield session


Session = Annotated[AsyncSession, Depends(get_db)]
