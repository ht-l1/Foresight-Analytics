import logging
from sqlalchemy.orm import Session
from app.models.company import Company

logger = logging.getLogger(__name__)

# check if the company exists in the database
def get_company_by_symbol(db: Session, symbol: str) -> Company | None:
    return db.query(Company).filter(Company.symbol == symbol).first()

def create_company_from_profile(db: Session, profile_data: dict) -> Company:
    """Create or update a company from FMP profile data."""
    
    # Define the data dictionary ONCE at the top.
    company_data = {
        'symbol': profile_data.get('symbol'),
        'company_name': profile_data.get('company_name'),
        'sector': profile_data.get('sector'),
        'industry': profile_data.get('industry'),
        'country': profile_data.get('country'),
        'full_time_employees': profile_data.get('full_time_employees'),
        'ceo': profile_data.get('ceo'),
        'price': profile_data.get('price'),
        'market_cap': profile_data.get('market_cap'),
        'beta': profile_data.get('beta'),
        'volume': profile_data.get('volume'),
        'average_volume': profile_data.get('average_volume'),
        'range_52_week': profile_data.get('range_52_week'),
        'last_dividend': profile_data.get('last_dividend'),
        'is_actively_trading': profile_data.get('is_actively_trading', True)
    }

    # Find the existing company
    existing = db.query(Company).filter(Company.symbol == company_data['symbol']).first()
    
    if existing:
        # If it exists, UPDATE it using the dictionary
        logger.info(f"Updating existing company: {company_data['symbol']}")
        for key, value in company_data.items():
            if value is not None:
                setattr(existing, key, value)
        
        db.commit()
        db.refresh(existing)
        return existing
    else:
        # If it doesn't exist, CREATE it using the dictionary
        logger.info(f"Creating new company: {company_data['symbol']}")
        # Filter out None values before creating
        filtered_data = {k: v for k, v in company_data.items() if v is not None}
        
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