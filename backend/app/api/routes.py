from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..core.database import get_db

router = APIRouter()

@router.get("/companies")
async def get_companies(db: Session = Depends(get_db)):
    companies = [
        {"symbol": "AAPL", "name": "Apple Inc."},
        {"symbol": "AMZN", "name": "Amazon.com Inc."},
        {"symbol": "GOOGL", "name": "Alphabet Inc."},
        {"symbol": "META", "name": "Meta Platforms Inc."},
        {"symbol": "NFLX", "name": "Netflix Inc."}
    ]
    return {"companies": companies}

@router.get("/test-db")
async def test_database(db: Session = Depends(get_db)):
    """Test database connection"""
    try:
        # Simple query to test connection
        db.execute("SELECT 1")
        return {"status": "Database connection successful"}
    except Exception as e:
        return {"status": "Database connection failed", "error": str(e)}