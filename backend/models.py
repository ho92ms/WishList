from __future__ import annotations

from typing import Optional

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class WishlistItem(Base):
    __tablename__ = "wishlist_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    city: Mapped[str] = mapped_column(String(80), index=True)
    poi_id: Mapped[str] = mapped_column(String(140), index=True)

    name: Mapped[str] = mapped_column(String(240))
    address: Mapped[Optional[str]] = mapped_column(String(400), nullable=True)

    tag: Mapped[str] = mapped_column(String(32), index=True)  # food/culture/nature

    created_at: Mapped[object] = mapped_column(DateTime(timezone=True), server_default=func.now())


class WeeklyReport(Base):
    __tablename__ = "weekly_reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    generated_at: Mapped[object] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # store JSON as string for simplicity
    payload_json: Mapped[str] = mapped_column(String)
