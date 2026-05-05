from datetime import datetime
from sqlalchemy import ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base


class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    follower_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    following_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default="now()", nullable=False
    )

    # Связи
    follower: Mapped["User"] = relationship(
        "User", foreign_keys=[follower_id], back_populates="subscriptions"
    )
    following: Mapped["User"] = relationship(
        "User", foreign_keys=[following_id], back_populates="followers"
    )

    __table_args__ = (
        UniqueConstraint("follower_id", "following_id", name="uq_subscription"),
    )
