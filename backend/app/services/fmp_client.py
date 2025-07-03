import aiohttp
import asyncio
from typing import Optional, Dict, List, Any
from datetime import datetime, timedelta
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class FMPClient:
    BASE_URL = "https://financialmodelingprep.com/stable"
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={'User-Agent': 'Foresight-Analytics/1.0'}
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def _make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make authenticated request to FMP API"""
        if not self.session:
            raise RuntimeError("FMPClient must be used as async context manager")
        
        url = f"{self.BASE_URL}/{endpoint}"
        request_params = {"apikey": self.api_key}
        
        if params:
            request_params.update(params)
        
        try:
            logger.info(f"Making request to FMP: {endpoint}")
            async with self.session.get(url, params=request_params) as response:
                
                # Handle rate limiting
                if response.status == 429:
                    logger.warning("Rate limit hit, waiting 60 seconds...")
                    await asyncio.sleep(60)
                    # Retry once
                    async with self.session.get(url, params=request_params) as retry_response:
                        retry_response.raise_for_status()
                        return await retry_response.json()
                
                response.raise_for_status()
                data = await response.json()
                
                # Handle FMP error responses
                if isinstance(data, dict) and "Error Message" in data:
                    raise ValueError(f"FMP API Error: {data['Error Message']}")
                
                return data
                
        except aiohttp.ClientError as e:
            logger.error(f"HTTP error for {endpoint}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error for {endpoint}: {e}")
            raise
    
    async def get_company_profile(self, symbol: str) -> Dict[str, Any]:
        data = await self._make_request(f"profile?symbol={symbol}")
        return data[0] if isinstance(data, list) and data else data
    
    async def get_income_statement(self, symbol: str, period: str = "quarter", limit: int = 20) -> List[Dict[str, Any]]:
        params = {"symbol": symbol, "period": period, "limit": min(limit, 120)}  # Add symbol here
        return await self._make_request("income-statement", params)

    async def get_balance_sheet(self, symbol: str, period: str = "quarter", limit: int = 20) -> List[Dict[str, Any]]:
        params = {"symbol": symbol, "period": period, "limit": min(limit, 120)}  # Add symbol here
        return await self._make_request("balance-sheet-statement", params)
    
    async def get_cash_flow(self, symbol: str, period: str = "quarter", limit: int = 20) -> List[Dict[str, Any]]:
        params = {"symbol": symbol, "period": period, "limit": min(limit, 120)}  # Add symbol here
        return await self._make_request("cash-flow-statement", params)
    
    async def get_revenue_segments(self, symbol: str) -> List[Dict[str, Any]]:
        return await self._make_request(f"revenue-product-segmentation", {"symbol": symbol})
    
    async def get_latest_articles(self, page: int = 0, size: int = 20) -> Dict[str, Any]:
        params = {"page": page, "size": min(size, 100)}  # Free tier limit
        return await self._make_request("fmp-articles", params)


# FAANG company symbols
FAANG_SYMBOLS = ["AAPL", "AMZN", "GOOGL", "META", "NFLX"]

async def get_fmp_client() -> FMPClient:
    """Factory function to create FMP client"""
    return FMPClient(api_key=settings.FMP_API_KEY)