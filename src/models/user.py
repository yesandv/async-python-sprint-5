from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, relationship

from src.db import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = Column(
        Integer, primary_key=True, autoincrement=True, unique=True
    )
    name: Mapped[str] = Column(String(50), nullable=False, unique=True)
    hashed_password: Mapped[str] = Column(String, nullable=False)
    files = relationship("FileModel", back_populates="user")
