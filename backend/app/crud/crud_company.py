import logging
from sqlalchemy.orm import Session
from app.models.company import Company

logger = logging.getLogger(__name__)

# check if the company exists in the database
def get_company_by_symbol(db: Session, symbol: str) -> Company | None:
    return db.query(Company).filter(Company.symbol == symbol).first()

def create_company_from_profile(db: Session, profile_data: dict) -> Company:
    """Create or update a company from FMP profile data."""
    
    symbol = profile_data.get('symbol')
    if not symbol:
        return None

    existing = get_company_by_symbol(db, symbol)
    
    if existing:
        # If it exists, UPDATE it using the dictionary
        logger.info(f"Updating existing company: {symbol}")
        for key, value in profile_data.items():
            if value is not None:
                setattr(existing, key, value)
        
        db.commit()
        db.refresh(existing)
        return existing
    else:
        # If it doesn't exist, CREATE it using the dictionary
        logger.info(f"Creating new company: {symbol}")
        # Filter out None values before creating
        filtered_data = {k: v for k, v in profile_data.items() if v is not None}
        
        company = Company(**filtered_data)
        db.add(company)
        db.commit()
        db.refresh(company)
        return company

def create_minimal_company(db: Session, symbol: str) -> Company:
    """Fallback function to create a minimal company record when profile fetch fails."""
    company = Company(symbol=symbol, company_name=f"Company {symbol}")
    db.add(company)
    db.commit()
    db.refresh(company)
    return company