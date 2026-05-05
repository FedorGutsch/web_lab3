from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(
        String(30), unique=True, index=True, nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    avatar_url: Mapped[Optional[str]] = mapped_column(String(2048), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default="now()", nullable=False
    )

    # Связи
    posts: Mapped[list["Post"]] = relationship(
        "Post", back_populates="author", cascade="all, delete-orphan"
    )
    reactions: Mapped[list["Reaction"]] = relationship(
        "Reaction", back_populates="user", cascade="all, delete-orphan"
    )

    # Подписки (many-to-many через таблицу subscriptions)
    subscriptions: Mapped[list["Subscription"]] = relationship(
        "Subscription",
        foreign_keys="[Subscription.follower_id]",
        back_populates="follower",
        cascade="all, delete-orphan",
    )
    followers: Mapped[list["Subscription"]] = relationship(
        "Subscription",
        foreign_keys="[Subscription.following_id]",
        back_populates="following",
        cascade="all, delete-orphan",
    )
