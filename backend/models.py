from sqlalchemy import Column, DateTime
from sqlalchemy import Integer, String, ForeignKey, Boolean
import enum
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from db import Base

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
    created_at = Column(DateTime, default=datetime.now)
