from sqlalchemy.orm import Session
from app.models.financials import IncomeStatement
from typing import List, Dict
from datetime import datetime

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