import aiohttp
import asyncio
import logging
from typing import Optional, Dict, List, Any
from pydantic import ValidationError

from app.core.config import settings
from app.core.exceptions import FMPAPIError, RateLimitError, DataValidationError
from app.schemas import fmp_schemas

logger = logging.getLogger(__name__)

class FMPClient:
    """
    An asynchronous client for the FMP API.
    Handles API requests, data validation, and error handling.
    """
    BASE_URL = settings.fmp_base_url

    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("FMPClient requires an API key for initialization.")
        self.api_key = api_key
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        """Asynchronous context manager to manage the client session."""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={'User-Agent': 'Foresight-Analytics/1.0'}
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Cleanly closes the client session."""
        if self.session:
            await self.session.close()

    async def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Internal method to make an authenticated request to the FMP API.
        It handles standard HTTP errors, API-specific errors, and rate limiting.
        """
        if not self.session:
            raise RuntimeError("FMPClient must be used as an async context manager for session management.")
        
        url = f"{self.BASE_URL}/{endpoint}"
        request_params = {"apikey": self.api_key}
        if params:
            request_params.update(params)
        
        try:
            logger.info(f"Requesting data from FMP endpoint: {endpoint} with params: {params}")
            async with self.session.get(url, params=request_params) as response:
                if response.status == 429:
                    logger.warning("FMP API rate limit exceeded.")
                    raise RateLimitError()
                
                response.raise_for_status() # Raises a ClientResponseError for 4xx/5xx statuses
                data = await response.json()
                
                if isinstance(data, dict) and "Error Message" in data:
                    logger.error(f"FMP API returned an error: {data['Error Message']}")
                    raise FMPAPIError(data["Error Message"])
                
                if not data:
                    logger.warning(f"No data returned from endpoint: {endpoint}")
                
                return data

        except aiohttp.ClientResponseError as http_err:
            logger.error(f"HTTP error for {endpoint}: {http_err.status} {http_err.message}")
            raise FMPAPIError(f"HTTP error occurred: {http_err.status}") from http_err
        except Exception as e:
            logger.error(f"An unexpected error occurred while requesting {endpoint}: {e}")
            raise # Re-raise after logging

    async def get_company_profile(self, symbol: str) -> fmp_schemas.CompanyProfile:
        try:
            params = {"symbol": symbol}
            data = await self._make_request("profile", params=params)
            if not data:
                raise FMPAPIError(f"No profile data found for symbol: {symbol}")
            # The FMP profile endpoint returns a list containing a single object
            return fmp_schemas.CompanyProfile.model_validate(data[0])
        except ValidationError as e:
            logger.error(f"Data validation failed for {symbol} CompanyProfile: {e.errors()}")
            raise DataValidationError(model="CompanyProfile", errors=e.errors())
        except FMPAPIError as e:
            logger.warning(f"Could not fetch profile for {symbol}: {e.message}")
            raise

    async def get_income_statement(self, symbol: str, period: str = "annual", limit: int = 5) -> List[fmp_schemas.IncomeStatement]:
        params = {"symbol": symbol, "period": period, "limit": limit}
        try:
            data = await self._make_request("income-statement", params)
            return [fmp_schemas.IncomeStatement.model_validate(item) for item in data]
        except ValidationError as e:
            logger.error(f"Data validation failed for {symbol} IncomeStatements: {e.errors()}")
            raise DataValidationError(model="IncomeStatementList", errors=e.errors())

    async def get_balance_sheet_statement(self, symbol: str, period: str = "annual", limit: int = 5) -> List[fmp_schemas.BalanceSheetStatement]:
        try:
            params = {"symbol": symbol, "period": period, "limit": limit}
            data = await self._make_request("balance-sheet-statement", params)
            return [fmp_schemas.BalanceSheetStatement.model_validate(item) for item in data]
        except ValidationError as e:
            logger.error(f"Data validation failed for {symbol} BalanceSheetStatements: {e.errors()}")
            raise DataValidationError(model="BalanceSheetStatementList", errors=e.errors())

    async def get_cash_flow_statement(self, symbol: str, period: str = "annual", limit: int = 5) -> List[fmp_schemas.CashFlowStatement]:
        params = {"symbol": symbol, "period": period, "limit": limit}
        try:
            data = await self._make_request("cash-flow-statement", params)
            return [fmp_schemas.CashFlowStatement.model_validate(item) for item in data]
        except ValidationError as e:
            logger.error(f"Data validation failed for {symbol} CashFlowStatements: {e.errors()}")
            raise DataValidationError(model="CashFlowStatementList", errors=e.errors())

    async def get_revenue_segments(self, symbol: str, period: str = "annual") -> List[fmp_schemas.RevenueSegment]:
        params = {"symbol": symbol, "period": period}
        try:
            raw_data = await self._make_request("revenue-product-segmentation", params)
            segments = []

            for item in raw_data:
                base_fields = {
                    "symbol": item["symbol"],
                    "fiscal_Year": str(item["fiscalYear"]),
                    "period": item["period"],
                    "date": item["date"], 
                }

                for segment_name, segment_revenue in item.get("data", {}).items():
                    segment = fmp_schemas.RevenueSegment(
                        **base_fields,
                        segment_Name=segment_name,
                        segment_Revenue=segment_revenue,
                    )
                    segments.append(segment)

            return segments

        except ValidationError as e:
            logger.error(f"Data validation failed for {symbol} RevenueSegments: {e.errors()}")
            raise DataValidationError(model="RevenueSegmentList", errors=e.errors())

    async def get_fmp_articles(self, page: int = 0, limit: int = settings.fmp_max_articles) -> List[fmp_schemas.FMPArticle]:
        params = {"page": page, "limit": limit}
        try:
            data = await self._make_request("fmp-articles", params)
            return [fmp_schemas.FMPArticle.model_validate(item) for item in data]
        except ValidationError as e:
            logger.error(f"Data validation failed for FMP Articles: {e.errors()}")
            raise DataValidationError(model="FMPArticleList", errors=e.errors())
        
    async def get_key_metrics(self, symbol: str, period: str = "annual", limit: int = 40) -> list[fmp_schemas.KeyMetrics]:
        params = {"period": period, "limit": limit}
        return await self._get(f"key-metrics/{symbol}", params=params, response_model=list[fmp_schemas.KeyMetrics])

    async def get_financial_ratios(self, symbol: str, period: str = "annual", limit: int = 40) -> list[fmp_schemas.FinancialRatios]:
        params = {"period": period, "limit": limit}
        return await self._get(f"ratios/{symbol}", params=params, response_model=list[fmp_schemas.FinancialRatios])

    async def get_key_metrics_ttm(self, symbol: str) -> fmp_schemas.KeyMetricsTTM:
        response = await self._get(f"key-metrics-ttm/{symbol}", response_model=list[fmp_schemas.KeyMetricsTTM])
        if not response:
            raise ValueError(f"No TTM key metrics found for symbol: {symbol}")
        return response[0]

    async def get_financial_ratios_ttm(self, symbol: str) -> fmp_schemas.FinancialRatiosTTM:
        response = await self._get(f"ratios-ttm/{symbol}", response_model=list[fmp_schemas.FinancialRatiosTTM])
        if not response:
            raise ValueError(f"No TTM financial ratios found for symbol: {symbol}")
        return response[0]