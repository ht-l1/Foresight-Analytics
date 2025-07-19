import aiohttp
import logging
from typing import Optional, Dict, List, Any
from fastapi import HTTPException
from app.core.config import settings
from app.schemas import fmp_schemas
from pydantic import ValidationError

logger = logging.getLogger(__name__)

class FMPClient:
    """
    An asynchronous client for the FMP API.
    """
    BASE_URL = settings.fmp_base_url

    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("FMPClient requires an API key")
        self.api_key = api_key
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        """Asynchronous context manager to manage the client session."""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=10),
            headers={'User-Agent': 'Foresight-Analytics/1.0'}
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Make an authenticated request to the FMP API."""
        if not self.session:
            raise RuntimeError("FMPClient must be used as an async context manager")
        
        url = f"{self.BASE_URL}/{endpoint}"
        request_params = {"apikey": self.api_key}
        if params:
            request_params.update(params)
        
        try:
            logger.info(f"Requesting data from FMP endpoint: {endpoint}")
            async with self.session.get(url, params=request_params) as response:
                if response.status == 429:
                    raise HTTPException(status_code=429, detail="FMP API rate limit exceeded")
                
                response.raise_for_status()
                data = await response.json()
                
                if isinstance(data, dict) and "Error Message" in data:
                    raise HTTPException(status_code=400, detail=f"FMP API error: {data['Error Message']}")
                
                return data or []
                
        except aiohttp.ClientResponseError as e:
            raise HTTPException(status_code=e.status, detail=f"FMP API error: {e.message}")

    async def get_company_profile(self, symbol: str) -> fmp_schemas.CompanyProfile:
        """Get company profile data."""
        data = await self._make_request(f"profile/{symbol}")
        
        if not data:
            raise HTTPException(status_code=404, detail=f"No profile data found for symbol: {symbol}")
        
        try:
            return fmp_schemas.CompanyProfile.model_validate(data[0])
        except ValidationError as e:
            logger.error(f"Data validation failed for {symbol} CompanyProfile: {e.errors()}")
            raise HTTPException(status_code=422, detail="Invalid data format from FMP API")

    async def get_income_statement(self, symbol: str, period: str = "annual", limit: int = 5):
        """Get income statement data."""
        params = {"symbol": symbol,"period": period, "limit": limit}
        data = await self._make_request("income-statement", params)
        
        try:
            return [fmp_schemas.IncomeStatement.model_validate(item) for item in data]
        except ValidationError as e:
            logger.error(f"Data validation failed for {symbol} IncomeStatement: {e.errors()}")
            raise HTTPException(status_code=422, detail="Invalid data format from FMP API")