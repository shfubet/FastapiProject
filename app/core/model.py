from datetime import datetime, timezone

from sqlalchemy.orm import sessionmaker, Session, relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import DateTime, Integer, Boolean


class Base(DeclarativeBase):
    pass


class ModelMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        comment="创建时间"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc),
        comment="更新时间"
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    is_delete: Mapped[bool] = mapped_column(Boolean, default=False, comment="逻辑删除")


class BaseModel(Base, ModelMixin):
    __abstract__ = True
