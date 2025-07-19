from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base

class TimestampMixin:
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Company(Base, TimestampMixin):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(10), unique=True, index=True, nullable=False)
    company_name = Column(String(200))
    # Business Context
    sector = Column(String(100))
    industry = Column(String(100))
    country = Column(String(50))
    full_time_employees = Column(String(20))  # API returns as string
    ceo = Column(String(200))
    # Current Market Data
    price = Column(Numeric(10, 2))
    market_cap = Column(Numeric(18, 2))
    beta = Column(Numeric(6, 4))
    # Trading Data
    volume = Column(Numeric(15, 0))
    average_volume = Column(Numeric(15, 0))
    range_52_week = Column(String(50))
    # Dividend Data
    last_dividend = Column(Numeric(8, 4))
    # Status
    is_actively_trading = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)
    # Relationships
    income_statements = relationship("IncomeStatement", back_populates="company")