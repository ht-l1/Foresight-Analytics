import logging
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.services.fmp_client import FMPClient
from app.crud.crud_company import get_company_by_symbol, create_company_from_profile, create_minimal_company
from app.crud.crud_financials import upsert_income_statements
from app.models.company import Company
from app.models.financials import IncomeStatement
from app.core.config import settings
from typing import List, Dict, Any
from fastapi import HTTPException
from datetime import datetime

logger = logging.getLogger(__name__)

# 1: get data INTO database (sync functions): Sync pulls data from the external API and pushes it into the DB.
# 2: get data OUT OF database (get functions): User makes request, and Get function retrieve data from the DB.

async def get_or_create_company(db: Session, symbol: str, fmp_client: FMPClient) -> Company:
    """Get existing company or create new one."""
    company = get_company_by_symbol(db, symbol)
    if company:
        return company
    
    logger.info(f"Creating new company record for {symbol}")
    try:
        profile_data = await fmp_client.get_company_profile(symbol)
        company = create_company_from_profile(db, profile_data.model_dump())
        logger.info(f"Successfully created company {symbol}")
    except Exception as e:
        logger.error(f"Failed to create company {symbol} from profile: {str(e)}")
        company = create_minimal_company(db, symbol)
    
    return company

async def sync_income_statements(db: Session, symbols: List[str], force_refresh: bool = False):
    """Sync income statements for given symbols."""
    logger.info(f"Starting income statement sync for {len(symbols)} symbols")
    
    async with FMPClient(api_key=settings.fmp_api_key) as fmp_client:
        for symbol in symbols:
            try:
                logger.info(f"Syncing income statements for {symbol}")
                
                # Get or create company
                company = await get_or_create_company(db, symbol, fmp_client)
                
                # Get income statement data
                income_statements = await fmp_client.get_income_statement(
                    symbol=symbol, 
                    period="annual", 
                    limit=settings.fmp_max_periods
                )
                
                if not income_statements:
                    logger.warning(f"No income statement data found for {symbol}")
                    continue
                
                # Prepare data for database
                statements_to_insert = []
                for statement in income_statements:
                    statement_dict = statement.model_dump()
                    statement_dict['company_id'] = company.id
                    # Convert date string to date object
                    if 'date' in statement_dict:
                        statement_dict['date'] = datetime.strptime(statement_dict['date'], '%Y-%m-%d').date()
                    statements_to_insert.append(statement_dict)
                
                # Insert/update in database
                upsert_income_statements(db, statements_to_insert)
                logger.info(f"Successfully synced {len(statements_to_insert)} income statements for {symbol}")
                
            except Exception as e:
                logger.error(f"Failed to sync income statements for {symbol}: {str(e)}")
                continue
    
    logger.info("Income statement sync completed")

# SERVICE FUNCTIONS FOR ROUTES
def get_company_profile(db: Session, symbol: str) -> Dict[str, Any]:
    """Get company profile from database."""
    company = get_company_by_symbol(db, symbol)
    if not company:
        raise HTTPException(status_code=404, detail=f"Company with symbol {symbol} not found")
    
    return {
        "id": company.id,
        "symbol": company.symbol,
        "company_name": company.company_name,
        "sector": company.sector,
        "industry": company.industry,
        "country": company.country,
        "full_time_employees": company.full_time_employees,
        "ceo": company.ceo,
        "price": float(company.price) if company.price else None,
        "market_cap": float(company.market_cap) if company.market_cap else None,
        "beta": float(company.beta) if company.beta else None,
        "volume": float(company.volume) if company.volume else None,
        "average_volume": float(company.average_volume) if company.average_volume else None,
        "range_52_week": company.range_52_week,
        "last_dividend": float(company.last_dividend) if company.last_dividend else None,
        "is_actively_trading": company.is_actively_trading,
        "created_at": company.created_at.isoformat() if company.created_at else None,
        "updated_at": company.updated_at.isoformat() if company.updated_at else None,
    }

def get_income_statements(db: Session, symbol: str, skip: int = 0, limit: int = 20) -> Dict[str, Any]:
    """Get paginated income statements for a symbol."""
    # Get total count
    total = db.query(IncomeStatement).filter(IncomeStatement.symbol == symbol).count()
    
    # Get paginated data
    statements = (
        db.query(IncomeStatement)
        .filter(IncomeStatement.symbol == symbol)
        .order_by(desc(IncomeStatement.date))
        .offset(skip)
        .limit(limit)
        .all()
    )
    
    if not statements:
        raise HTTPException(status_code=404, detail=f"No income statements found for symbol {symbol}")
    
    items = []
    for stmt in statements:
        items.append({
            "id": stmt.id,
            "symbol": stmt.symbol,
            "date": stmt.date.isoformat() if stmt.date else None,
            "fiscal_year": stmt.fiscal_year,
            "period": stmt.period,
            "reported_currency": stmt.reported_currency,
            "revenue": float(stmt.revenue) if stmt.revenue else None,
            "cost_of_revenue": float(stmt.cost_of_revenue) if stmt.cost_of_revenue else None,
            "gross_profit": float(stmt.gross_profit) if stmt.gross_profit else None,
            "operating_expenses": float(stmt.operating_expenses) if stmt.operating_expenses else None,
            "operating_income": float(stmt.operating_income) if stmt.operating_income else None,
            "net_income": float(stmt.net_income) if stmt.net_income else None,
            "eps": float(stmt.eps) if stmt.eps else None,
            "eps_diluted": float(stmt.eps_diluted) if stmt.eps_diluted else None,
            "ebitda": float(stmt.ebitda) if stmt.ebitda else None,
            "ebit": float(stmt.ebit) if stmt.ebit else None,
        })
    
    return {
        "items": items,
        "total": total,
        "skip": skip,
        "limit": limit,
        "has_more": skip + limit < total
    }