import logging
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from app.core.config import settings
from app.services.fmp_client import FMPClient
from app.models.financial import Company, IncomeStatement, BalanceSheetStatement, CashFlowStatement, RevenueSegment, NewsArticle
from app.schemas.fmp_schemas import CompanyProfile as FMPCompanyProfile, IncomeStatement as FMPIncomeStatement, BalanceSheetStatement as FMPBalanceSheet, CashFlowStatement as FMPCashFlow, RevenueSegment as FMPRevenueSegment, FMPArticle

logger = logging.getLogger(__name__)

async def get_or_create_company(db: Session, symbol: str, fmp_client: FMPClient) -> Company:
    """
    Retrieves a company from the DB or creates it if it doesn't exist,
    fetching its profile from FMP.
    """
    company = db.query(Company).filter(Company.symbol == symbol).first()
    if not company:
        logger.info(f"Company {symbol} not found in DB. Fetching from FMP...")
        profile_data: FMPCompanyProfile = await fmp_client.get_company_profile(symbol)
        
        company = Company(
            symbol=profile_data.symbol,
            name=profile_data.companyName,
            sector=profile_data.sector,
            industry=profile_data.industry,
            market_cap=profile_data.mktCap,
            country=profile_data.country,
            is_active=profile_data.isActivelyTrading
        )
        db.add(company)
        db.commit()
        db.refresh(company)
        logger.info(f"Company {symbol} created in DB.")
    return company

async def sync_income_statements(db: Session, company: Company, fmp_client: FMPClient):
    """Fetches and upserts income statements for a company."""
    logger.info(f"Syncing income statements for {company.symbol}")
    statements_data: list[FMPIncomeStatement] = await fmp_client.get_income_statement(
        symbol=company.symbol, limit=settings.fmp_max_periods
    )
    
    if not statements_data:
        logger.warning(f"No income statements found for {company.symbol}")
        return

    insert_stmt = insert(IncomeStatement).values([
        {
            "company_id": company.id,
            "symbol": stmt.symbol,
            "date": stmt.date,
            "period": stmt.period,
            "calendar_year": stmt.calendarYear,
            "revenue": stmt.revenue,
            "net_income": stmt.netIncome,
            "eps": stmt.eps,
            "epsdiluted": stmt.epsdiluted,
        } for stmt in statements_data
    ])

    # Upsert logic: if symbol, date, and period conflict, do nothing.
    upsert_stmt = insert_stmt.on_conflict_do_nothing(
        index_elements=['symbol', 'date', 'period']
    )
    db.execute(upsert_stmt)
    db.commit()
    logger.info(f"Successfully upserted {len(statements_data)} income statements for {company.symbol}")


async def sync_balance_sheet_statements(db: Session, company: Company, fmp_client: FMPClient):
    """Fetches and upserts balance sheet statements for a company."""
    logger.info(f"Syncing balance sheet statements for {company.symbol}")
    statements_data: list[FMPBalanceSheet] = await fmp_client.get_balance_sheet_statement(
        symbol=company.symbol, limit=settings.fmp_max_periods
    )

    if not statements_data:
        logger.warning(f"No balance sheet statements found for {company.symbol}")
        return

    insert_stmt = insert(BalanceSheetStatement).values([
        {
            "company_id": company.id,
            "symbol": stmt.symbol,
            "date": stmt.date,
            "period": stmt.period,
            "calendar_year": stmt.calendarYear,
            "total_assets": stmt.totalAssets,
            "total_liabilities": stmt.totalLiabilities,
            "total_stockholders_equity": stmt.totalStockholdersEquity,
        } for stmt in statements_data
    ])
    
    upsert_stmt = insert_stmt.on_conflict_do_nothing(
        index_elements=['symbol', 'date', 'period']
    )
    db.execute(upsert_stmt)
    db.commit()
    logger.info(f"Successfully upserted {len(statements_data)} balance sheet statements for {company.symbol}")


async def sync_cash_flow_statements(db: Session, company: Company, fmp_client: FMPClient):
    """Fetches and upserts cash flow statements for a company."""
    logger.info(f"Syncing cash flow statements for {company.symbol}")
    statements_data: list[FMPCashFlow] = await fmp_client.get_cash_flow_statement(
        symbol=company.symbol, limit=settings.fmp_max_periods
    )

    if not statements_data:
        logger.warning(f"No cash flow statements found for {company.symbol}")
        return

    insert_stmt = insert(CashFlowStatement).values([
        {
            "company_id": company.id,
            "symbol": stmt.symbol,
            "date": stmt.date,
            "period": stmt.period,
            "calendar_year": stmt.calendarYear,
            "net_cash_provided_by_operating_activities": stmt.netCashProvidedByOperatingActivities,
            "net_cash_used_for_investing_activities": stmt.netCashUsedForInvestingActivites,
            "net_cash_used_by_financing_activities": stmt.netCashUsedProvidedByFinancingActivities,
        } for stmt in statements_data
    ])
    
    upsert_stmt = insert_stmt.on_conflict_do_nothing(
        index_elements=['symbol', 'date', 'period']
    )
    db.execute(upsert_stmt)
    db.commit()
    logger.info(f"Successfully upserted {len(statements_data)} cash flow statements for {company.symbol}")

async def sync_all_financials_for_symbol(symbol: str, db: Session):
    """
    Orchestrates the fetching and storing of all financial data for a single company.
    """
    logger.info(f"Starting financial data sync for {symbol}...")
    async with FMPClient(api_key=settings.fmp_api_key) as fmp_client:
        try:
            # Get or create the company record
            company = await get_or_create_company(db, symbol, fmp_client)
            
            # Sync each statement type
            await sync_income_statements(db, company, fmp_client)
            await sync_balance_sheet_statements(db, company, fmp_client)
            await sync_cash_flow_statements(db, company, fmp_client)

            logger.info(f"Completed financial data sync for {symbol}.")

        except Exception as e:
            logger.error(f"Failed to sync data for {symbol}: {e}", exc_info=True)
            db.rollback()

async def sync_revenue_segments(db: Session, company: Company, fmp_client: FMPClient):
    """Fetches and upserts revenue segmentation for a company."""
    logger.info(f"Syncing revenue segments for {company.symbol}")
    try:
        segments_data: list[RevenueSegment] = await fmp_client.get_revenue_segments(symbol=company.symbol)
        
        if not segments_data:
            logger.warning(f"No revenue segments found for {company.symbol}")
            return

        insert_stmt = insert(RevenueSegment).values([
            {
                "company_id": company.id,
                "symbol": seg.symbol,
                "date": seg.date,
                "segment_name": seg.segment,
                "revenue": seg.revenue,
            } for seg in segments_data
        ])

        upsert_stmt = insert_stmt.on_conflict_do_nothing(
            index_elements=['symbol', 'date', 'segment_name']
        )
        db.execute(upsert_stmt)
        db.commit()
        logger.info(f"Successfully upserted {len(segments_data)} revenue segments for {company.symbol}")

    except Exception as e:
        logger.error(f"Could not sync revenue segments for {company.symbol}: {e}", exc_info=True)
        db.rollback()


async def sync_articles(db: Session, symbols: list[str], fmp_client: FMPClient):
    """Fetches and upserts news articles for a list of symbols."""
    logger.info(f"Syncing news articles for symbols: {', '.join(symbols)}")
    try:
        articles_data: list[FMPArticle] = await fmp_client.get_stock_news(
            symbols=symbols, limit=settings.fmp_max_articles
        )
        
        if not articles_data:
            logger.warning("No new articles found.")
            return

        # map article symbols to company_ids
        companies = db.query(Company).filter(Company.symbol.in_(symbols)).all()
        symbol_to_id_map = {c.symbol: c.id for c in companies}

        insert_stmt = insert(NewsArticle).values([
            {
                "company_id": symbol_to_id_map.get(art.symbol),
                "symbol": art.symbol,
                "title": art.title,
                "url": art.url,
                "text": art.text,
                "published_date": art.publishedDate,
                "site": art.site,
            } for art in articles_data if symbol_to_id_map.get(art.symbol) is not None
        ])

        upsert_stmt = insert_stmt.on_conflict_do_nothing(index_elements=['url'])
        db.execute(upsert_stmt)
        db.commit()
        logger.info(f"Successfully upserted {len(articles_data)} articles.")

    except Exception as e:
        logger.error(f"Could not sync articles: {e}", exc_info=True)
        db.rollback()