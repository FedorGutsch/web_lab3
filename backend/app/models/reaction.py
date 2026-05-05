from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import ForeignKey, DateTime, Enum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
import enum


class ReactionType(str, PyEnum):
    like = "like"
    heart = "heart"
    fire = "fire"
    smile = "smile"


class Reaction(Base):
    __tablename__ = "reactions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    post_id: Mapped[int] = mapped_column(
        ForeignKey("posts.id", ondelete="CASCADE"), index=True
    )
    reaction_type: Mapped[ReactionType] = mapped_column(
        Enum(ReactionType), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default="now()", nullable=False
    )

    # Связи
    user: Mapped["User"] = relationship("User", back_populates="reactions")
    post: Mapped["Post"] = relationship("Post", back_populates="reactions")

    __table_args__ = (
        UniqueConstraint("user_id", "post_id", name="uq_user_post_reaction"),
    )
