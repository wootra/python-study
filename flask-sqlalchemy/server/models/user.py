from typing import List
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..config import db
from .email import Email


class User(db.Model):
    id: Mapped[Integer] = mapped_column(Integer, primary_key=True)
    username: Mapped[String] = mapped_column(
        String, unique=True, nullable=False)
    emails: Mapped[List[Email]] = relationship(
        Email,
        backref="user",
        lazy=True,
        cascade="all, delete-orphan",
    )
