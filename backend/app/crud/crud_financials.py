from sqlalchemy.orm import Session
from typing import List, Dict
from datetime import datetime
from ..models.financials import IncomeStatement, FinancialRatio, KeyMetric 
from ..schemas.fmp_schemas import FMPIncomeStatement, FinancialRatios, KeyMetrics

def upsert_income_statements(db: Session, income_statements: List[Dict]):
    """Insert or update income statements."""
    if not income_statements:
        return
    
    for data in income_statements:
        # Convert date string to date object if it's a string
        if 'date' in data and isinstance(data['date'], str):
            data['date'] = datetime.strptime(data['date'], '%Y-%m-%d').date()
        
        # Check if record exists
        existing = db.query(IncomeStatement).filter_by(
            symbol=data['symbol'], 
            date=data['date'], 
            period=data['period']
        ).first()
        
        if existing:
            # Update existing record
            for key, value in data.items():
                setattr(existing, key, value)
        else:
            # Create new record
            income_statement = IncomeStatement(**data)
            db.add(income_statement)
    
    db.commit()

def create_financial_ratios(db: Session, ratios: list[FinancialRatios], company_id: int, symbol: str) -> list[FinancialRatio]:
    """
    Creates new financial ratio records in bulk.
    """
    db_ratios = [
        FinancialRatio(
            company_id=company_id,
            symbol=symbol,
            date=item.date,
            period=item.period,
            **item.model_dump(exclude={'symbol', 'date', 'period'}, by_alias=False)
        )
        for item in ratios
    ]
    db.bulk_save_objects(db_ratios)
    db.commit()
    return db_ratios

def create_key_metrics(db: Session, metrics: list[KeyMetrics], company_id: int, symbol: str) -> list[KeyMetric]:
    """
    Creates new key metric records in bulk.
    """
    db_metrics = [
        KeyMetric(
            company_id=company_id,
            symbol=symbol,
            date=item.date,
            period=item.period,
            **item.model_dump(exclude={'symbol', 'date', 'period'}, by_alias=False)
        )
        for item in metrics
    ]
    db.bulk_save_objects(db_metrics)
    db.commit()
    return db_metrics