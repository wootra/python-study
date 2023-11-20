from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from ..config import db


class Email(db.Model):
    id: Mapped[Integer] = mapped_column(Integer, primary_key=True)
    email: Mapped[String] = mapped_column(String, unique=True, nullable=False)
    user_id: Mapped[Integer] = mapped_column(
        Integer, db.ForeignKey("user.id"), nullable=False
    )
