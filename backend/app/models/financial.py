from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base

class Company(Base):
# Company Profile API
# https://site.financialmodelingprep.com/developer/docs/companies-key-stats-free-api

    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(10), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False) #api: companyName
    sector = Column(String(100))
    industry = Column(String(100))
    market_cap = Column(Float)   #api: mktCap
    country = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    income_statements = relationship("IncomeStatement", back_populates="company")
    balance_sheet_statements = relationship("BalanceSheetStatement", back_populates="company")
    cash_flow_statements = relationship("CashFlowStatement", back_populates="company")
    revenue_segments = relationship("RevenueSegment", back_populates="company")
    predictions = relationship("MLPrediction", back_populates="company")

class IncomeStatement(Base):
    __tablename__ = 'income_statements'
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    symbol = Column(String(10), index=True, nullable=False)
    date = Column(Date, nullable=False, index=True)
    period = Column(String(10), nullable=False)
    calendar_year = Column(String(4), nullable=False)
    revenue = Column(Float)
    cost_of_revenue = Column(Float)
    gross_profit = Column(Float)
    net_income = Column(Float)
    eps = Column(Float)
    epsdiluted = Column(Float)
    
    company = relationship("Company", back_populates="income_statements")

class BalanceSheetStatement(Base):
    __tablename__ = 'balance_sheet_statements'
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    symbol = Column(String(10), index=True, nullable=False)
    date = Column(Date, nullable=False, index=True)
    period = Column(String(10), nullable=False)
    calendar_year = Column(String(4), nullable=False)
    total_assets = Column(Float)
    total_liabilities = Column(Float)
    total_stockholders_equity = Column(Float)
    
    company = relationship("Company", back_populates="balance_sheet_statements")

class CashFlowStatement(Base):
    __tablename__ = 'cash_flow_statements'
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    symbol = Column(String(10), index=True, nullable=False)
    date = Column(Date, nullable=False, index=True)
    period = Column(String(10), nullable=False)
    calendar_year = Column(String(4), nullable=False)
    net_cash_provided_by_operating_activities = Column(Float)
    net_cash_used_for_investing_activities = Column(Float)
    net_cash_used_by_financing_activities = Column(Float)
    
    company = relationship("Company", back_populates="cash_flow_statements")

class RevenueSegment(Base):
# Revenue Product Segmentation API
# Revenue Geographic Segments API
    __tablename__ = "revenue_segments"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    symbol = Column(String(10), index=True, nullable=False)
    
    # Time period
    date = Column(DateTime, nullable=False, index=True)
    period = Column(String(10), nullable=False)
    calendar_year = Column(Integer, nullable=False)
    
    # Segment information
    segment_name = Column(String(255), nullable=False)
    segment_type = Column(String(50))  # geographic, product, business_unit
    segment_revenue = Column(Float)
    segment_percentage = Column(Float)  # % of total revenue
    
    # Growth metrics
    segment_growth_yoy = Column(Float)
    segment_growth_qoq = Column(Float)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    company = relationship("Company", back_populates="revenue_segments")

class MLPrediction(Base):
    __tablename__ = "ml_predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    symbol = Column(String(10), index=True, nullable=False)
    
    # Prediction details
    model_name = Column(String(50), nullable=False)  # moving_average, prophet, linear_regression
    model_version = Column(String(20), default="1.0")
    target_metric = Column(String(50), nullable=False)  # revenue, net_income, etc.
    
    # Prediction period
    prediction_date = Column(DateTime, nullable=False, index=True)
    prediction_period = Column(String(10), nullable=False)  # Q1, Q2, Q3, Q4
    prediction_year = Column(Integer, nullable=False)
    
    # Prediction values
    predicted_value = Column(Float, nullable=False)
    confidence_interval_lower = Column(Float)
    confidence_interval_upper = Column(Float)
    confidence_score = Column(Float)  # 0-1 score
    
    # Model performance metrics
    training_rmse = Column(Float)
    training_mape = Column(Float)
    training_r2 = Column(Float)
    
    # Actual vs predicted (filled after actual results)
    actual_value = Column(Float)
    prediction_error = Column(Float)
    absolute_percentage_error = Column(Float)
    
    # Model metadata
    training_data_points = Column(Integer)
    features_used = Column(Text)  # JSON string of features
    model_parameters = Column(Text)  # JSON string of hyperparameters
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    company = relationship("Company", back_populates="predictions")

class NewsArticle(Base):
# FMP Articles API
    __tablename__ = "news_articles"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Article details
    title = Column(String(500), nullable=False)
    url = Column(String(1000), unique=True, nullable=False)
    published_date = Column(DateTime, nullable=False, index=True)
    author = Column(String(255))
    source = Column(String(100))
    
    # Content
    snippet = Column(Text)
    content = Column(Text)
    
    # Analysis
    sentiment_score = Column(Float)  # -1 to 1 (negative to positive)
    sentiment_label = Column(String(20))  # negative, neutral, positive
    relevance_score = Column(Float)  # 0-1 relevance to finance
    
    # Associated companies (many-to-many relationship via tags)
    mentioned_symbols = Column(String(200))  # Comma-separated list
    
    # Processing status
    is_processed = Column(Boolean, default=False)
    processing_error = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class ModelPerformance(Base):
    __tablename__ = "model_performance"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Model identification
    model_name = Column(String(50), nullable=False)
    model_version = Column(String(20), default="1.0")
    target_metric = Column(String(50), nullable=False)
    
    # Performance period
    evaluation_date = Column(DateTime, nullable=False, index=True)
    evaluation_period_start = Column(DateTime, nullable=False)
    evaluation_period_end = Column(DateTime, nullable=False)
    
    # Performance metrics
    rmse = Column(Float)
    mape = Column(Float)
    mae = Column(Float)  # Mean Absolute Error
    r2_score = Column(Float)
    predictions_count = Column(Integer)
    
    # Model comparison
    rank_by_rmse = Column(Integer)
    rank_by_mape = Column(Integer)
    is_best_model = Column(Boolean, default=False)
    
    # Additional metadata
    companies_evaluated = Column(String(200))  # Comma-separated symbols
    notes = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# Create indexes for performance
from sqlalchemy import Index

# Composite indexes for common queries
Index('idx_income_statements_symbol_date', IncomeStatement.symbol, IncomeStatement.date)
Index('idx_balance_sheet_statements_symbol_date', BalanceSheetStatement.symbol, BalanceSheetStatement.date)
Index('idx_cash_flow_statements_symbol_date', CashFlowStatement.symbol, CashFlowStatement.date)
Index('idx_revenue_segments_symbol_date', RevenueSegment.symbol, RevenueSegment.date)
Index('idx_predictions_symbol_date', MLPrediction.symbol, MLPrediction.prediction_date)
Index('idx_news_published_sentiment', NewsArticle.published_date, NewsArticle.sentiment_score)