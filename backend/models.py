from sqlalchemy import Column, DateTime
from sqlalchemy import Integer, String, ForeignKey, Boolean
import enum
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from db import Base
from sqlalchemy_file.file import File
from sqlalchemy_file.types import FileField

class ChatRole(str, enum.Enum):
    SYSTEM = "system"
    ASSISTANT = "assistant"
    USER = "user"

class Chat(Base):
    __tablename__ = 'chat'

    id = Column(Integer, primary_key=True, index=True)
    message: Mapped[str]
    role: Mapped[ChatRole] = mapped_column(
        sa.Enum(ChatRole), nullable=False)
    file_id: Mapped[int] = mapped_column(ForeignKey('video.id'), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)


class Video(Base):
    __tablename__ = 'video'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    file_data: Mapped[File] = mapped_column(FileField, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)