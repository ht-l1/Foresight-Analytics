# can delete later
# Test FMP client with all main endpoints for AAPL

import asyncio
import os
from app.services.fmp_client import FMPClient, FAANG_SYMBOLS

async def test_fmp_client():
    api_key = os.getenv("FMP_API_KEY")
    if not api_key:
        print("❌ FMP_API_KEY not found in environment variables")
        print("Please add FMP_API_KEY to your .env file")
        return

    print(f"🔑 Using FMP API key from environment (hidden for security)...")

    async with FMPClient(api_key) as client:
        try:
            symbol = "AAPL"

            # Company Profile
            print("\n📊 Testing company profile...")
            profile = await client.get_company_profile(symbol)
            print(f"✅ Company: {profile.get('companyName', 'N/A')}")
            print(f"   Sector: {profile.get('sector', 'N/A')}")
            print(f"   Market Cap: ${profile.get('mktCap', 0):,}")

            # Income Statement (last 4 quarters)
            print("\n📈 Testing income statement (last 4 quarters)...")
            income_data = await client.get_income_statement(symbol, period="quarter", limit=4)
            if income_data:
                print(f"✅ Retrieved {len(income_data)} quarters of income statement")
                for i, quarter in enumerate(income_data[:2]):
                    revenue = quarter.get('revenue', 0)
                    date = quarter.get('date', 'N/A')
                    print(f"   Q{i+1} ({date}): Revenue ${revenue:,}")
            else:
                print("❌ No income statement data received")

            # Balance Sheet (last 4 quarters)
            print("\n💰 Testing balance sheet (last 4 quarters)...")
            balance_data = await client.get_balance_sheet(symbol, period="quarter", limit=4)
            if balance_data:
                print(f"✅ Retrieved {len(balance_data)} quarters of balance sheet")
                for i, quarter in enumerate(balance_data[:2]):
                    total_assets = quarter.get('totalAssets', 0)
                    date = quarter.get('date', 'N/A')
                    print(f"   Q{i+1} ({date}): Total Assets ${total_assets:,}")
            else:
                print("❌ No balance sheet data received")

            # Cash Flow (last 4 quarters)
            print("\n💵 Testing cash flow statement (last 4 quarters)...")
            cashflow_data = await client.get_cash_flow(symbol, period="quarter", limit=4)
            if cashflow_data:
                print(f"✅ Retrieved {len(cashflow_data)} quarters of cash flow")
                for i, quarter in enumerate(cashflow_data[:2]):
                    operating_cash_flow = quarter.get('operatingCashFlow', 0)
                    date = quarter.get('date', 'N/A')
                    print(f"   Q{i+1} ({date}): Operating Cash Flow ${operating_cash_flow:,}")
            else:
                print("❌ No cash flow data received")

            # Revenue Segments
            print("\n📊 Testing revenue segments...")
            revenue_segments = await client.get_revenue_segments(symbol)
            if revenue_segments:
                print(f"✅ Retrieved {len(revenue_segments)} revenue segments")
                for segment in revenue_segments[:3]:
                    name = segment.get('segment', 'N/A')
                    revenue = segment.get('revenue', 0)
                    print(f"   Segment: {name}, Revenue: ${revenue:,}")
            else:
                print("❌ No revenue segment data received")

            # Latest Articles
            print("\n📰 Testing latest articles...")
            articles = await client.get_latest_articles(size=3)
            if isinstance(articles, list) and articles:
                print(f"✅ Retrieved {len(articles)} articles")
                for i, article in enumerate(articles[:3]):
                    title = article.get('title', 'N/A')[:70]
                    published = article.get('publishedDate', 'N/A')
                    print(f"   {i+1}. {title} (Published: {published})")
            else:
                print("❌ No articles data received")

        except Exception as e:
            print(f"❌ Error testing FMP client: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_fmp_client())
