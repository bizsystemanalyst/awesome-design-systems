from sqlalchemy import Column, Date, DateTime, Float, Integer, String, UniqueConstraint
from sqlalchemy.sql import func

from .db import Base


class FitbitToken(Base):
    __tablename__ = 'fitbit_tokens'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False, unique=True)
    access_token = Column(String, nullable=False)
    refresh_token = Column(String, nullable=False)
    expires_at = Column(DateTime, nullable=True)
    scope = Column(String, nullable=True)
    token_type = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())


class DailyHealthMetric(Base):
    __tablename__ = 'daily_health_metrics'
    __table_args__ = (UniqueConstraint('user_id', 'date', name='uq_user_date_metric'),)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False)
    date = Column(Date, index=True, nullable=False)
    resting_heart_rate = Column(Float, nullable=True)
    sleep_minutes = Column(Integer, nullable=True)
    steps = Column(Integer, nullable=True)
    calories_out = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
