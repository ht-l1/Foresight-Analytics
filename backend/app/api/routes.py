from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from ..core.database import get_db
from ..core.config import settings
from ..services import data_service
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/financials/sync-faang", status_code=202)
async def sync_faang_financials(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    logger.info("Received request to sync FAANG financial data.")
    
    for symbol in settings.FAANG_SYMBOLS:
        background_tasks.add_task(data_service.sync_all_financials_for_symbol, symbol, db)
        
    return {"message": "FAANG financial data synchronization has been started in the background."}

@router.post("/financials/sync-faang-segments", status_code=202)
async def sync_faang_segments(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    logger.info("Received request to sync FAANG revenue segmentation data.")
    from app.services.fmp_client import FMPClient
    
    async def task():
        async with FMPClient(api_key=settings.fmp_api_key) as fmp_client:
            for symbol in settings.FAANG_SYMBOLS:
                company = await data_service.get_or_create_company(db, symbol, fmp_client)
                if company:
                    await data_service.sync_revenue_segments(db, company, fmp_client)

    background_tasks.add_task(task)
    return {"message": "FAANG revenue segment synchronization has been started."}

@router.post("/news/sync-faang-articles", status_code=202)
async def sync_faang_articles(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    logger.info("Received request to sync FAANG news articles.")
    from app.services.fmp_client import FMPClient

    async def task():
        async with FMPClient(api_key=settings.fmp_api_key) as fmp_client:
            await data_service.sync_articles(db, settings.FAANG_SYMBOLS, fmp_client)
            
    background_tasks.add_task(task)
    return {"message": "FAANG news article synchronization has been started."}

@router.get("/test-db")
async def test_database(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "Database connection successful"}
    except Exception as e:
        logger.error(f"Database connection test failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Database connection failed")