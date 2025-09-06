"""Query model."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.db.base import Base


class Query(Base):
    """Query model."""

    __tablename__ = "queries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    raw_text = Column(String, nullable=False)
    budget_min = Column(Numeric(10, 2), nullable=True)
    budget_max = Column(Numeric(10, 2), nullable=True)
    usage = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", backref="queries")
    rankings = relationship("Ranking", backref="query")
