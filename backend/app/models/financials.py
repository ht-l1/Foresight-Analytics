from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, UniqueConstraint, Index, Date
from sqlalchemy.orm import relationship
from ..core.database import Base

class TimestampMixin:
    created_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True))

class FinancialDataMixin:
    symbol = Column(String(10), index=True, nullable=False)
    date = Column(Date, nullable=False, index=True)
    fiscal_year = Column(String(4), nullable=False)
    period = Column(String(10), nullable=False)
    reported_currency = Column(String(3), default="USD")

class IncomeStatement(Base, FinancialDataMixin, TimestampMixin):
    __tablename__ = 'income_statements'
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey('companies.id'), index=True)
    revenue = Column(Numeric(18, 2))
    cost_of_revenue = Column(Numeric(18, 2))
    gross_profit = Column(Numeric(18, 2))
    research_and_development_expenses = Column(Numeric(18, 2))
    selling_general_and_administrative_expenses = Column(Numeric(18, 2))
    operating_expenses = Column(Numeric(18, 2))
    operating_income = Column(Numeric(18, 2))
    income_before_tax = Column(Numeric(18, 2))
    income_tax_expense = Column(Numeric(18, 2))
    net_income = Column(Numeric(18, 2))
    eps = Column(Numeric(8, 4))
    eps_diluted = Column(Numeric(8, 4))
    weighted_average_shs_out = Column(Numeric(15, 0))
    weighted_average_shs_out_dil = Column(Numeric(15, 0))
    ebitda = Column(Numeric(18, 2))
    ebit = Column(Numeric(18, 2))
    depreciation_and_amortization = Column(Numeric(18, 2))
    company = relationship("Company", back_populates="income_statements")
    __table_args__ = (
        UniqueConstraint('symbol', 'date', 'period', name='_symbol_date_period_uc_income'),
        Index('idx_income_symbol_fiscal_year', 'symbol', 'fiscal_year'),
    ) 