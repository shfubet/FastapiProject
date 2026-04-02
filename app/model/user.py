from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.model import BaseModel


class User(BaseModel):
    __tablename__ = "users"
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100), unique=True)
