from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, validates
from ..config import db


class Email(db.Model):
    id: Mapped[Integer] = mapped_column(Integer, primary_key=True)
    email: Mapped[String] = mapped_column(String, unique=True, nullable=False)
    user_id: Mapped[Integer] = mapped_column(
        Integer, db.ForeignKey("user.id"), nullable=False
    )

    @validates("email")
    def validate_email(self, key, email):
        if "@" not in email:
            raise ValueError("Invalid email address.")
        return email

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "user_id": self.user_id,
        }