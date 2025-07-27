# test with command docker-compose exec backend python tests/sync_test_data.py

import asyncio
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.database import SessionLocal
from app.services.business_service import (
    sync_company_profiles,
    sync_income_statements,
    sync_key_metrics,
    sync_financial_ratios,
    sync_stock_news,
)
from app.core.config import settings

async def main():
    symbols = settings.FAANG_SYMBOLS
    
    print("--- Starting Data Sync ---")
    
    # Sync each step with its own database session to avoid transaction rollback issues
    steps = [
        ("Company Profiles", sync_company_profiles),
        ("Income Statements", sync_income_statements),
        ("Key Metrics", sync_key_metrics),
        ("Financial Ratios", sync_financial_ratios),
        ("Stock News", sync_stock_news),
    ]
    
    for step_name, sync_function in steps:
        db = SessionLocal()
        try:
            print(f"\n{len(steps) - steps.index((step_name, sync_function)) + 1}. Syncing {step_name}...")
            await sync_function(db, symbols)
            print(f"✅ {step_name} sync completed successfully")
        except Exception as e:
            print(f"❌ {step_name} sync failed: {str(e)}")
            db.rollback()  # Rollback failed transaction
        finally:
            db.close()
    
    print("\n--- Data Sync Complete ---")

if __name__ == "__main__":
    asyncio.run(main())