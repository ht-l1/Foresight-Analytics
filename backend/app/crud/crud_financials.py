from sqlalchemy.orm import Session
from typing import List, Dict
from datetime import datetime
from ..models.financials import IncomeStatement as IncomeStatementModel, FinancialRatio, KeyMetric
from ..schemas.fmp_schemas import IncomeStatement as FMPIncomeStatement, FinancialRatios, KeyMetrics

def upsert_income_statements(db: Session, statements: List[Dict], company_id: int, symbol: str):
    """
    Upserts (updates or inserts) income statement records from processed data dictionaries.
    """
    for data_dict in statements:
        existing = db.query(IncomeStatementModel).filter_by(
            symbol=symbol, 
            date=data_dict['date'], 
            period=data_dict['period']
        ).first()

        if existing:
            # Update existing record
            for key, value in data_dict.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)
        else:
            # Create new record
            new_statement = IncomeStatementModel(**data_dict)
            db.add(new_statement)

    db.commit()

def upsert_financial_ratios(db: Session, ratios: List[Dict], company_id: int, symbol: str):
    """
    Upserts financial ratio records.
    """
    for data_dict in ratios:
        existing = db.query(FinancialRatio).filter_by(
            symbol=symbol,
            date=data_dict['date'],
            period=data_dict['period']
        ).first()
        
        if existing:
            for key, value in data_dict.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)
        else:
            new_ratio = FinancialRatio(**data_dict)
            db.add(new_ratio)
    
    db.commit()

def upsert_key_metrics(db: Session, metrics: List[Dict], company_id: int, symbol: str):
    """
    Upserts key metric records.
    """
    for data_dict in metrics:
        existing = db.query(KeyMetric).filter_by(
            symbol=symbol,
            date=data_dict['date'],
            period=data_dict['period']
        ).first()
        
        if existing:
            for key, value in data_dict.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)
        else:
            new_metric = KeyMetric(**data_dict)
            db.add(new_metric)
    
    db.commit()