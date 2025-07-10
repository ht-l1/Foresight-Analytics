import logging
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import inspect
from app.core.config import settings
from app.services.fmp_client import FMPClient
from app.models.financial import Company, IncomeStatement, BalanceSheetStatement, CashFlowStatement, RevenueSegment, NewsArticle
from app.schemas.fmp_schemas import CompanyProfile as FMPCompanyProfile, IncomeStatement as FMPIncomeStatement, BalanceSheetStatement as FMPBalanceSheet, CashFlowStatement as FMPCashFlow, RevenueSegment as FMPRevenueSegment, FMPArticle

logger = logging.getLogger(__name__)

async def get_or_create_company(db: Session, symbol: str, fmp_client: FMPClient) -> Company:
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
    logger.info(f"Syncing income statements for {company.symbol}")
    statements_data: list[FMPIncomeStatement] = await fmp_client.get_income_statement(
        symbol=company.symbol, period="FY", limit=settings.fmp_max_periods
    )
    
    if not statements_data:
        logger.warning(f"No income statements found for {company.symbol}")
        return
    
    values_to_insert = []
    for stmt in statements_data:
        values_to_insert.append({
            "company_id": company.id,
            "symbol": stmt.symbol,
            "date": stmt.report_date, 
            "period": stmt.period,
            "fiscal_year": stmt.fiscal_Year,
            "revenue": stmt.revenue,
            "cost_of_revenue": stmt.cost_Of_Revenue,
            "gross_profit": stmt.gross_Profit,
            "net_income": stmt.net_Income,
            "eps": stmt.eps,
            "epsdiluted": stmt.eps_diluted,  # Use snake_case here
        })

    if not values_to_insert:
        logger.info(f"No new income statements to insert for {company.symbol}.")
        return

    # Use the prepared list of dictionaries to create the insert statement
    insert_stmt = insert(IncomeStatement).values(values_to_insert)

    # Upsert logic: if symbol, date, and period conflict, do nothing.
    upsert_stmt = insert_stmt.on_conflict_do_nothing(
        index_elements=['symbol', 'date', 'period']
    )
    db.execute(upsert_stmt)
    db.commit()
    logger.info(f"Successfully upserted {len(statements_data)} income statements for {company.symbol}")

async def sync_balance_sheet_statements(db: Session, company: Company, fmp_client: FMPClient):
    logger.info(f"Syncing balance sheet statements for {company.symbol}")
    statements_data: list[FMPBalanceSheet] = await fmp_client.get_balance_sheet_statement(
        symbol=company.symbol, period="FY", limit=settings.fmp_max_periods
    )

    if not statements_data:
        logger.warning(f"No balance sheet statements found for {company.symbol}")
        return

    insert_stmt = insert(BalanceSheetStatement).values([
        {
            "company_id": company.id,
            "symbol": stmt.symbol,
            "date": stmt.report_date,
            "period": stmt.period,
            "fiscal_year": stmt.fiscal_Year,
            "total_assets": stmt.total_Assets,
            "total_liabilities": stmt.total_Liabilities,
            "total_stockholders_equity": stmt.total_Stockholders_Equity,
        } for stmt in statements_data
    ])
    
    upsert_stmt = insert_stmt.on_conflict_do_nothing(
        index_elements=['symbol', 'date', 'period']
    )
    db.execute(upsert_stmt)
    db.commit()
    logger.info(f"Successfully upserted {len(statements_data)} balance sheet statements for {company.symbol}")


async def sync_cash_flow_statements(db: Session, company: Company, fmp_client: FMPClient):
    logger.info(f"Syncing cash flow statements for {company.symbol}")
    statements_data: list[FMPCashFlow] = await fmp_client.get_cash_flow_statement(
        symbol=company.symbol, period="FY", limit=settings.fmp_max_periods
    )

    if not statements_data:
        logger.warning(f"No cash flow statements found for {company.symbol}")
        return

    insert_stmt = insert(CashFlowStatement).values([
        {
            "company_id": company.id,
            "symbol": stmt.symbol,
            "date": stmt.report_date,
            "period": stmt.period,
            "fiscal_year": stmt.fiscal_Year,
            "net_cash_provided_by_operating_activities": stmt.net_Cash_Provided_By_Operating_Activities,
            "net_cash_used_for_investing_activities": stmt.net_Cash_Used_For_Investing_Activities,
            "net_cash_used_by_financing_activities": stmt.net_Cash_Used_Provided_By_Financing_Activities,
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
    logger.info(f"Syncing revenue segments for {company.symbol}")
    try:
        segments_data: list[RevenueSegment] = await fmp_client.get_revenue_segments(symbol=company.symbol, period="FY")
        
        if not segments_data:
            logger.warning(f"No revenue segments found for {company.symbol}")
            return

        insert_stmt = insert(RevenueSegment).values([
            {
                "company_id": company.id,
                "symbol": seg.symbol,
                "fiscal_Year": seg.fiscal_Year,
                "period": seg.period,
                "date": seg.report_date,
                "segment_name": seg.segment_Name,
                "segment_revenue": seg.segment_Revenue,
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
    logger.info(f"Syncing news articles for symbols: {', '.join(symbols)}")
    try:
        articles_data: list[FMPArticle] = await fmp_client.get_fmp_articles(
            limit=settings.fmp_max_articles
        )
        
        if not articles_data:
            logger.warning("No new articles found.")
            return

        # Extract symbols from tickers field and map to company_ids
        companies = db.query(Company).filter(Company.symbol.in_(symbols)).all()
        symbol_to_id_map = {c.symbol: c.id for c in companies}

        articles_to_insert = []
        for art in articles_data:
            # Extract symbol from tickers (e.g., "NASDAQ:WING" -> "WING")
            if hasattr(art, 'tickers') and art.tickers:
                symbol = art.tickers.split(':')[-1]  # Get the part after ':'
                company_id = symbol_to_id_map.get(symbol)
                
                if company_id is not None:
                    articles_to_insert.append({
                        "title": art.title,
                        "url": art.url,
                        "published_date": art.published_Date,
                        "author": art.author,
                        "source": art.source,
                        "snippet": art.snippet,
                        "mentioned_symbols": symbol, 
                    })

        if articles_to_insert:
            insert_stmt = insert(NewsArticle).values(articles_to_insert)
            upsert_stmt = insert_stmt.on_conflict_do_nothing(index_elements=['url'])
            db.execute(upsert_stmt)
            db.commit()
            logger.info(f"Successfully upserted {len(articles_to_insert)} articles.")
        else:
            logger.warning("No articles matched the requested symbols.")

    except Exception as e:
        logger.error(f"Could not sync articles: {e}", exc_info=True)
        db.rollback()