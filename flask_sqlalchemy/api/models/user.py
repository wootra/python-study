from typing import List
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy_serializer import SerializerMixin
from ..config import db
from .email import Email


class User(db.Model, SerializerMixin):
    id: Mapped[Integer] = mapped_column(Integer, primary_key=True)
    username: Mapped[String] = mapped_column(
        String, unique=True, nullable=False)
    emails: Mapped[List[Email]] = relationship(
        Email,
        backref="user",
        lazy=True,
        cascade="all, delete-orphan",
    )

    @validates("username")
    def validate_username(self, key, username):
        if not username:
            raise ValueError("Username is required.")
        return username
