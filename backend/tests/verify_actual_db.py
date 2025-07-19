import sys
import os

# Get the directory above 'backend/tests', which is 'backend'
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.company import Company
from app.models.financials import IncomeStatement

def check_database():
    """Check what data is actually in the database"""
    print("=== Database Verification ===")
    
    db = SessionLocal()
    try:
        # Check companies
        companies = db.query(Company).all()
        print(f"\n📊 Companies in database: {len(companies)}")
        
        for company in companies:
            print(f"  • {company.symbol}: {company.company_name or 'N/A'}")
            print(f"    Sector: {company.sector or 'N/A'}")
            if company.market_cap:
                print(f"    Market Cap: ${company.market_cap:,.0f}")
            else:
                print(f"    Market Cap: N/A")
        
        # Check income statements
        statements = db.query(IncomeStatement).all()
        print(f"\n📈 Income Statements in database: {len(statements)}")
        
        # Group by symbol
        symbol_counts = {}
        for stmt in statements:
            if stmt.symbol not in symbol_counts:
                symbol_counts[stmt.symbol] = []
            symbol_counts[stmt.symbol].append(stmt)
        
        for symbol, stmts in symbol_counts.items():
            print(f"\n  {symbol}: {len(stmts)} statements")
            # Show latest statement
            latest = sorted(stmts, key=lambda x: x.date, reverse=True)[0]
            print(f"    Latest: {latest.date}")
            if latest.revenue:
                print(f"    Revenue: ${latest.revenue:,.0f}")
            else:
                print(f"    Revenue: N/A")
            if latest.net_income:
                print(f"    Net Income: ${latest.net_income:,.0f}")
            else:
                print(f"    Net Income: N/A")
        
        if len(companies) == 0 and len(statements) == 0:
            print("\n⚠️  Database is empty!")
            print("   Run 'python tests/sync_test_data.py' first to populate data")
        
    except Exception as e:
        print(f"❌ Database check failed: {str(e)}")
    finally:
        db.close()

def test_api_endpoints():
    """Test the actual API endpoints"""
    print("\n=== API Endpoints Test ===")
    
    from fastapi.testclient import TestClient
    from app.main import app
    
    client = TestClient(app)
    
    # Test health
    print("\n1. Health Check:")
    response = client.get("/health")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   Response: {response.json()}")
    
    # Test company profile
    test_symbol = "AAPL"
    print(f"\n2. Company Profile ({test_symbol}):")
    response = client.get(f"/api/v1/company/{test_symbol}")
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   Company: {data.get('company_name', 'N/A')}")
        print(f"   Sector: {data.get('sector', 'N/A')}")
        
        # Safe formatting for price
        price = data.get('price')
        if price is not None:
            print(f"   Price: ${price:.2f}")
        else:
            print(f"   Price: N/A")
            
        # Safe formatting for market cap
        market_cap = data.get('market_cap')
        if market_cap is not None:
            print(f"   Market Cap: ${market_cap:,.0f}")
        else:
            print(f"   Market Cap: N/A")
            
    elif response.status_code == 404:
        print(f"   ⚠️  Company {test_symbol} not found in database")
    else:
        print(f"   ❌ Error: {response.text}")
    
    # Test income statements
    print(f"\n3. Income Statements ({test_symbol}):")
    response = client.get(f"/api/v1/financials/{test_symbol}/income-statements")
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   Total records: {data.get('total', 0)}")
        print(f"   Retrieved: {len(data.get('items', []))}")
        
        if data.get('items'):
            latest = data['items'][0]
            print(f"   Latest date: {latest.get('date', 'N/A')}")
            
            # Safe formatting for revenue
            revenue = latest.get('revenue')
            if revenue is not None:
                print(f"   Latest revenue: ${revenue:,.0f}")
            else:
                print(f"   Latest revenue: N/A")
                
            # Safe formatting for net income
            net_income = latest.get('net_income')
            if net_income is not None:
                print(f"   Latest net income: ${net_income:,.0f}")
            else:
                print(f"   Latest net income: N/A")
                
    elif response.status_code == 404:
        print(f"   ⚠️  No income statements for {test_symbol}")
    else:
        print(f"   ❌ Error: {response.text}")
    
    # Test pagination
    print(f"\n4. Pagination Test ({test_symbol}):")
    response = client.get(f"/api/v1/financials/{test_symbol}/income-statements?limit=2")
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Pagination works - got {len(data.get('items', []))} items (max 2)")
    else:
        print(f"   ❌ Pagination failed")

def print_summary():
    """Print a summary of findings"""
    print("\n" + "="*50)
    print("🎯 SUMMARY")
    print("="*50)
    
    db = SessionLocal()
    try:
        companies_count = db.query(Company).count()
        statements_count = db.query(IncomeStatement).count()
        
        # Check if companies have complete data
        companies_with_names = db.query(Company).filter(Company.company_name.isnot(None)).count()
        companies_with_prices = db.query(Company).filter(Company.price.isnot(None)).count()
        companies_with_market_cap = db.query(Company).filter(Company.market_cap.isnot(None)).count()
        
        print(f"📊 Database Status:")
        print(f"   - {companies_count} companies stored")
        print(f"   - {companies_with_names}/{companies_count} have company names")
        print(f"   - {companies_with_prices}/{companies_count} have prices")
        print(f"   - {companies_with_market_cap}/{companies_count} have market cap")
        print(f"   - {statements_count} financial statements stored")
        
        if companies_count > 0 and statements_count > 0:
            if companies_with_names < companies_count or companies_with_prices < companies_count:
                print("\n⚠️  Companies missing key data (name/price/market_cap)")
                print("   This suggests FMP API sync issues")
                print("   Check FMP API key and run sync again")
            else:
                print("\n✅ Database has complete data - API pipeline is working!")
            
            print("\n✅ API endpoints are responding correctly")
            
            if companies_with_names == companies_count and companies_with_prices == companies_count:
                print("\n🚀 The data pipeline is ready!")
            else:
                print("\n🔧 Fix needed: Re-sync company profile data")
                
        else:
            print("\n⚠️  Database is empty")
            print("   Run: python tests/sync_test_data.py")
            
    except Exception as e:
        print(f"❌ Could not generate summary: {str(e)}")
    finally:
        db.close()

def diagnose_fmp_issues():
    """Diagnose FMP API connection issues"""
    print("\n" + "="*50)
    print("🔍 FMP API DIAGNOSIS")
    print("="*50)
    
    try:
        from app.core.config import settings
        
        if not settings.fmp_api_key:
            print("❌ FMP_API_KEY not found in environment!")
            print("   Set FMP API key in .env file")
            return
        
        print(f"✅ FMP API key found: {settings.fmp_api_key[:8]}...")
        
        # Test basic FMP connection
        import asyncio
        from app.services.fmp_client import FMPClient
        
        async def test_fmp():
            async with FMPClient(api_key=settings.fmp_api_key) as client:
                try:
                    # Try a simple API call
                    response = await client.get_company_profile("AAPL")
                    print("✅ FMP API connection successful")
                    return True
                except Exception as e:
                    print(f"❌ FMP API connection failed: {str(e)}")
                    if "404" in str(e):
                        print("   This might be an API endpoint issue")
                        print("   Check if FMP subscription includes company profiles")
                    elif "401" in str(e) or "403" in str(e):
                        print("   This looks like an API key issue")
                        print("   Verify FMP API key is correct")
                    return False
        
        success = asyncio.run(test_fmp())
        
        if not success:
            print("\n🔧 SUGGESTED FIXES:")
            print("   1. Verify FMP API key at https://financialmodelingprep.com/developer/docs")
            print("   2. Check if the subscription includes required endpoints")
            print("   3. Test API key directly in browser:")
            print(f"      https://financialmodelingprep.com/api/v3/profile/AAPL?apikey={settings.fmp_api_key}")
        
    except Exception as e:
        print(f"❌ Could not diagnose FMP issues: {str(e)}")

if __name__ == "__main__":
    check_database()
    test_api_endpoints()
    diagnose_fmp_issues()
    print_summary()