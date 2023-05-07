from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, relationship

from src.db import Base


class FileModel(Base):
    __tablename__ = "files"

    id: Mapped[int] = Column(
        Integer, primary_key=True, autoincrement=True, unique=True
    )
    name: Mapped[str] = Column(String(50), nullable=False)
    size: Mapped[int] = Column(Integer)
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)
    created_by: Mapped[int] = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    is_deleted: Mapped[bool] = Column(Boolean, nullable=False, default=False)
    user = relationship("UserModel", back_populates="files")
