import datetime
from dataclasses import dataclass
from hashlib import sha256
from typing import Optional

from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.store.database.sqlalchemy_base import db


@dataclass
class User:
    id: int
    email: str
    referral_code: Optional[str] = None
    password: Optional[str] = None

    @staticmethod
    def hash_password(password: str) -> str:
        return sha256(password.encode()).hexdigest()

    def is_password_valid(self, password: str):
        return self.password == sha256(password.encode()).hexdigest()

    @classmethod
    def from_session(cls, session: Optional[dict]) -> Optional["User"]:
        return cls(id=session["user"]["id"], email=session["user"]["email"])


@dataclass
class AccessToken:
    id: int
    token: str
    user_id: int
    created_at: datetime.datetime
    expiration_date: datetime.datetime


class UserModel(db):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(120), unique=True)
    password: Mapped[str] = mapped_column(String(120), nullable=False)
    referral_code: Mapped[str] = mapped_column(String(120), nullable=True)


class AccessTokenModel(db):
    __tablename__ = "access_token"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(String(500), unique=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    expiration_date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
