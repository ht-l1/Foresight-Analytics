from typing import Optional, List 
from pydantic import BaseModel, Field, ConfigDict

class BaseFMPModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        extra='ignore'
    )

class CompanyProfile(BaseFMPModel):
    symbol: str
    company_name: str = Field(alias="companyName")
    price: float | None = None
    market_cap: float | None = Field(None, alias="marketCap")
    beta: float | None = None
    last_dividend: float | None = Field(None, alias="lastDividend")
    range_52_week: str | None = Field(None, alias="range")
    volume: float | None = None
    average_volume: float | None = Field(None, alias="averageVolume")
    ceo: str | None = None
    sector: str | None = None
    industry: str | None = None
    country: str | None = None
    full_time_employees: str | None = Field(None, alias="fullTimeEmployees")
    is_actively_trading: bool | None = Field(None, alias="isActivelyTrading")

class IncomeStatement(BaseFMPModel):
    symbol: str
    date: str
    fiscal_year: str = Field(alias="fiscalYear")
    period: str
    reported_currency: str | None = Field(None, alias="reportedCurrency")
    revenue: float | None = None
    cost_of_revenue: float | None = Field(None, alias="costOfRevenue")
    gross_profit: float | None = Field(None, alias="grossProfit")
    research_and_development_expenses: float | None = Field(None, alias="researchAndDevelopmentExpenses")
    selling_general_and_administrative_expenses: float | None = Field(None, alias="sellingGeneralAndAdministrativeExpenses")
    operating_expenses: float | None = Field(None, alias="operatingExpenses")
    operating_income: float | None = Field(None, alias="operatingIncome")
    income_before_tax: float | None = Field(None, alias="incomeBeforeTax")
    income_tax_expense: float | None = Field(None, alias="incomeTaxExpense")
    net_income: float | None = Field(None, alias="netIncome")
    eps: float | None = None
    eps_diluted: float | None = Field(None, alias="epsDiluted")
    weighted_average_shs_out: float | None = Field(None, alias="weightedAverageShsOut")
    weighted_average_shs_out_dil: float | None = Field(None, alias="weightedAverageShsOutDil")
    ebitda: float | None = None
    ebit: float | None = None
    depreciation_and_amortization: float | None = Field(None, alias="depreciationAndAmortization")

class FinancialRatios(BaseFMPModel):
    symbol: str
    date: str
    period: str
    net_profit_margin: Optional[float] = Field(None, alias="netProfitMargin")
    gross_profit_margin: Optional[float] = Field(None, alias="grossProfitMargin")
    return_on_equity: Optional[float] = Field(None, alias="returnOnEquity")
    price_to_earnings_ratio: Optional[float] = Field(None, alias="priceToEarningsRatio")
    price_to_book_ratio: Optional[float] = Field(None, alias="priceToBookRatio")
    price_to_sales_ratio: Optional[float] = Field(None, alias="priceToSalesRatio")
    ev_to_ebitda: Optional[float] = Field(None, alias="enterpriseValueMultiple")
    debt_to_equity_ratio: Optional[float] = Field(None, alias="debtToEquityRatio")
    current_ratio: Optional[float] = Field(None, alias="currentRatio")
    quick_ratio: Optional[float] = Field(None, alias="quickRatio")
    asset_turnover: Optional[float] = Field(None, alias="assetTurnover")
    inventory_turnover: Optional[float] = Field(None, alias="inventoryTurnover")

class KeyMetrics(BaseFMPModel):
    symbol: str
    date: str
    period: str
    market_cap: Optional[float] = Field(None, alias="marketCap")
    enterprise_value: Optional[float] = Field(None, alias="enterpriseValue")
    pe_ratio: Optional[float] = Field(None, alias="peRatio")
    pb_ratio: Optional[float] = Field(None, alias="pbRatio")
    dividend_yield: Optional[float] = Field(None, alias="dividendYield")
    free_cash_flow_yield: Optional[float] = Field(None, alias="freeCashFlowYield")
    return_on_equity: Optional[float] = Field(None, alias="returnOnEquity")
    debt_to_equity: Optional[float] = Field(None, alias="debtToEquity")

class FMPArticle(BaseFMPModel):
    title: str
    date: str
    content: str
    tickers: str
    image: str
    link: str
    author: str
    site: str