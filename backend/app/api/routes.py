from fastapi import APIRouter, Query, Path, HTTPException, Depends
from enum import Enum
from sqlalchemy.orm import Session
from ..core.database import get_db
from app.services.business_service import (
    get_company_profile,
    get_income_statements,
    get_key_metrics,
    get_financial_ratios,
    get_stock_news,
)
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class FinancialDataType(str, Enum):
    income_statements = "income-statements"
    key_metrics = "key-metrics"
    ratios = "ratios"

DATA_TYPE_TO_SERVICE = {
    FinancialDataType.income_statements: get_income_statements,
    FinancialDataType.key_metrics: get_key_metrics,
    FinancialDataType.ratios: get_financial_ratios,
}

@router.get("/company/{symbol}")
def company_profile(symbol: str, db: Session = Depends(get_db)):
    """Get company profile by symbol."""
    return get_company_profile(db, symbol)

@router.get("/financials/{symbol}/{data_type}")
def financials_paginated(
    symbol: str,
    data_type: FinancialDataType = Path(..., description="Type of financial data to retrieve"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get paginated financial data (income statements) for a symbol."""
    service_func = DATA_TYPE_TO_SERVICE.get(data_type)
    if not service_func:
        raise HTTPException(status_code=400, detail=f"Invalid data type: {data_type}")
    return service_func(db, symbol, skip, limit)

@router.get("/news/{symbol}")
def stock_news(symbol: str, limit: int = Query(20, ge=1, le=50), db: Session = Depends(get_db)):
    """Get latest news articles for a symbol."""
    return get_stock_news(db, symbol, limit)