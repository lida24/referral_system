import datetime
from dataclasses import dataclass
from hashlib import sha256
from typing import Optional

from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.store.database.sqlalchemy_base import db


@dataclass
class User:
    id: int
    email: str
    password: str
    referral_code_id: int | None = None

    @staticmethod
    def hash_password(password: str) -> str:
        return sha256(password.encode()).hexdigest()

    def is_password_valid(self, password: str):
        return self.password == sha256(password.encode()).hexdigest()

    @classmethod
    def from_session(cls, session: Optional[dict]) -> Optional["User"]:
        return cls(id=session["user"]["id"], email=session["user"]["email"])


@dataclass
class ReferralCode:
    id: int
    token: str
    created_at: datetime.datetime
    expiration_date: datetime.datetime
    user_id: int


@dataclass
class Referral:
    id: int
    email: str
    password: str
    referral_code_id: int
    referrer_id: int


class UserModel(db):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(120), unique=True)
    password: Mapped[str] = mapped_column(String(120), nullable=False)
    referral_code_id: Mapped[int] = mapped_column(ForeignKey("referral_codes.id", ondelete="SET NULL"), nullable=True)
    referral_code = relationship("ReferralCodeModel", foreign_keys=referral_code_id)


class ReferralCodeModel(db):
    __tablename__ = "referral_codes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(String(500), unique=True, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    expiration_date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = relationship("UserModel", foreign_keys=user_id)


class ReferralModel(db):
    __tablename__ = "referrals"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(120), unique=True)
    password: Mapped[str] = mapped_column(String(120), nullable=False)
    referral_code_id: Mapped[int] = mapped_column(ForeignKey("referral_codes.id", ondelete="CASCADE"))
    referrer_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
