"""Offer model."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric
from app.db.base import Base


class Offer(Base):
    """Offer model."""

    __tablename__ = "offers"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    price_cents = Column(Integer, nullable=False)
    currency = Column(String(3), default="USD", nullable=False)
    availability = Column(String, nullable=True)
    last_checked_at = Column(DateTime, default=datetime.utcnow, nullable=False)
