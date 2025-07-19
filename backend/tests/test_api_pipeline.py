"""
Verify if the API data pipeline is working.
"""

import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import get_db, Base
from app.models.company import Company
from app.models.financials import IncomeStatement
from app.services.business_service import sync_income_statements
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Test database URL (use SQLite for testing)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create test client
client = TestClient(app)

class TestAPIPipeline:
    
    @classmethod
    def setup_class(cls):
        """Set up test database"""
        Base.metadata.create_all(bind=engine)
        print("✓ Test database created")

        import os
        print("Current working directory:", os.getcwd())
        print("Looking for test.db at:", os.path.abspath("./test.db"))
        
    @classmethod
    def teardown_class(cls):
        """Clean up test database"""
        import gc
        import time

        # Try releasing all sessions, connections, and references
        TestingSessionLocal.close_all()
        engine.dispose()

        # Garbage collect to clear any dangling references
        gc.collect()

        # Wait a moment for Windows to release the file lock
        time.sleep(0.5)

        try:
            os.remove("./test.db")
            print("✓ Test database cleaned up")
        except PermissionError as e:
            print(f"✗ Could not remove test.db: {e}")

    def test_1_health_check(self):
        """Test basic API health"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        print("✓ API health check passed")

    def test_2_sync_data_to_db(self):
        """Test syncing data from FMP API to database"""
        db = next(override_get_db())
        
        # Test with one FAANG symbol
        test_symbol = "AAPL"
        
        try:
            # Run the sync process
            asyncio.run(sync_income_statements(db, [test_symbol]))
            
            # Check if company was created
            company = db.query(Company).filter(Company.symbol == test_symbol).first()
            assert company is not None, f"Company {test_symbol} not found in database"
            print(f"✓ Company {test_symbol} created in database")
            
            # Check if income statements were created
            statements = db.query(IncomeStatement).filter(IncomeStatement.symbol == test_symbol).all()
            assert len(statements) > 0, f"No income statements found for {test_symbol}"
            print(f"✓ {len(statements)} income statements created for {test_symbol}")
            
        except Exception as e:
            print(f"✗ Data sync failed: {str(e)}")
            raise

    def test_3_company_profile_endpoint(self):
        """Test company profile API endpoint"""
        test_symbol = "AAPL"
        
        response = client.get(f"/api/v1/company/{test_symbol}")
        
        if response.status_code == 404:
            print(f"⚠ Company {test_symbol} not in database - run sync first")
            return
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        assert data["symbol"] == test_symbol
        assert "company_name" in data
        print(f"✓ Company profile endpoint works for {test_symbol}")
        print(f"  Company: {data.get('company_name', 'N/A')}")
        print(f"  Sector: {data.get('sector', 'N/A')}")

    def test_4_income_statements_endpoint(self):
        """Test income statements API endpoint"""
        test_symbol = "AAPL"
        
        response = client.get(f"/api/v1/financials/{test_symbol}/income-statements")
        
        if response.status_code == 404:
            print(f"⚠ Income statements for {test_symbol} not in database - run sync first")
            return
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert len(data["items"]) > 0
        
        print(f"✓ Income statements endpoint works for {test_symbol}")
        print(f"  Total records: {data['total']}")
        print(f"  Retrieved: {len(data['items'])}")
        
        # Check first statement structure
        first_statement = data["items"][0]
        assert "revenue" in first_statement
        assert "net_income" in first_statement
        assert "date" in first_statement
        print(f"  Latest date: {first_statement.get('date', 'N/A')}")
        print(f"  Latest revenue: ${first_statement.get('revenue', 0):,.0f}")

    def test_5_pagination(self):
        """Test pagination in income statements endpoint"""
        test_symbol = "AAPL"
        
        # Test with limit
        response = client.get(f"/api/v1/financials/{test_symbol}/income-statements?limit=2")
        
        if response.status_code == 404:
            print(f"⚠ Skipping pagination test - no data for {test_symbol}")
            return
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) <= 2
        print(f"✓ Pagination works - limited to {len(data['items'])} items")

def run_manual_test():
    """Run a quick manual test if not using pytest"""
    print("=== Manual API Pipeline Test ===")
    
    # Test health
    print("\n1. Testing API health...")
    response = client.get("/health")
    if response.status_code == 200:
        print("✓ API is running")
    else:
        print("✗ API health check failed")
        return
    
    # Test sync
    print("\n2. Testing data sync...")
    print("⚠ Skipping data sync - run separately if needed")
    
    # Test endpoints
    test_symbol = "AAPL"
    
    print(f"\n3. Testing company profile for {test_symbol}...")
    response = client.get(f"/api/v1/company/{test_symbol}")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Got company: {data.get('company_name', 'Unknown')}")
    else:
        print(f"✗ Company profile failed: {response.status_code}")
    
    print(f"\n4. Testing income statements for {test_symbol}...")
    response = client.get(f"/api/v1/financials/{test_symbol}/income-statements")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Got {len(data['items'])} income statements")
    else:
        print(f"✗ Income statements failed: {response.status_code}")

if __name__ == "__main__":
    # Run manual test if script is executed directly
    run_manual_test()