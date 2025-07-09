from pydantic import BaseModel, Field, AnyHttpUrl,field_validator, ConfigDict
from typing import Optional, List
from datetime import datetime, date
from pydantic.alias_generators import to_camel

class CompanyProfile(BaseModel):
    symbol: str = Field(..., description="The stock symbol of the company.")
    price: Optional[float] = Field(None, description="Current stock price.")
    beta: Optional[float] = Field(None, description="Beta of the stock.")
    volAvg: Optional[int] = Field(None, description="Average trading volume.")
    mktCap: Optional[int] = Field(None, description="Market capitalization.")
    lastDiv: Optional[float] = Field(None, description="Last dividend paid.")
    range: Optional[str] = Field(None, description="52-week trading range.")
    changes: Optional[float] = Field(None, description="Recent price change.")
    companyName: str = Field(..., description="The name of the company.")
    currency: Optional[str] = Field(None, description="The currency the financials are reported in.")
    cik: Optional[str] = Field(None, description="CIK number.")
    isin: Optional[str] = Field(None, description="ISIN number.")
    cusip: Optional[str] = Field(None, description="CUSIP number.")
    exchange: Optional[str] = Field(None, description="The stock exchange where the company is listed.")
    exchangeShortName: Optional[str] = Field(None, description="Abbreviated name of the stock exchange.")
    industry: Optional[str] = Field(None, description="The industry the company belongs to.")
    website: Optional[str] = Field(None, description="Company's official website URL.")
    description: Optional[str] = Field(None, description="A description of the company's business.")
    ceo: Optional[str] = Field(None, description="Name of the CEO.")
    sector: Optional[str] = Field(None, description="The sector the company belongs to.")
    country: Optional[str] = Field(None, description="The country where the company is headquartered.")
    fullTimeEmployees: Optional[str] = Field(None, description="Number of full-time employees.")
    phone: Optional[str] = Field(None, description="Company's phone number.")
    address: Optional[str] = Field(None, description="Company's physical address.")
    city: Optional[str] = Field(None, description="City of the company's headquarters.")
    state: Optional[str] = Field(None, description="State of the company's headquarters.")
    zip: Optional[str] = Field(None, description="Zip code of the company's headquarters.")
    dcfDiff: Optional[float] = Field(None, alias="dcfDiff", description="DCF difference.")
    dcf: Optional[float] = Field(None, description="Discounted Cash Flow value.")
    image: Optional[str] = Field(None, description="URL of the company's logo.")
    ipoDate: Optional[date] = Field(None, description="Initial Public Offering date.")
    defaultImage: bool = Field(False, description="Indicates if the image is a default one.")
    isEtf: bool = Field(False, description="Indicates if the security is an ETF.")
    isActivelyTrading: bool = Field(False, description="Indicates if the company is actively trading.")
    isAdr: bool = Field(False, description="Indicates if the security is an ADR.")
    isFund: bool = Field(False, description="Indicates if the security is a fund.")

    @field_validator('ipoDate', mode='before')
    @classmethod
    def parse_ipo_date(cls, v):
        if isinstance(v, str) and v:
            try:
                return datetime.strptime(v, '%Y-%m-%d').date()
            except ValueError:
                return None
        return v

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )

class IncomeStatement(BaseModel):
    report_date: date = Field(..., alias='date', description="The date of the financial statement.")
    symbol: str = Field(..., description="The stock symbol.")
    reported_Currency: str = Field(..., description="The currency the statement is reported in.")
    cik: str = Field(..., description="CIK number.")
    filing_Date: date = Field(..., description="The date the statement was filed.")
    accepted_Date: datetime = Field(..., description="The date the filing was accepted.")
    fiscal_Year: str = Field(..., description="The fiscal year of the report.")
    period: str = Field(..., description="The reporting period (e.g., 'Q1', 'FY').")
    revenue: float = Field(..., description="Total revenue.")
    cost_Of_Revenue: float = Field(..., description="Cost of revenue.")
    gross_Profit: float = Field(..., description="Gross profit.")
    # gross_Profit_Ratio: float = Field(..., description="Gross profit ratio.")
    research_And_Development_Expenses: float = Field(..., description="R&D expenses.")
    general_And_Administrative_Expenses: float = Field(..., description="G&A expenses.")
    selling_And_Marketing_Expenses: float = Field(..., description="S&M expenses.")
    selling_General_And_Administrative_Expenses: float = Field(..., description="SG&A expenses.")
    other_Expenses: float = Field(..., description="Other operating expenses.")
    operating_Expenses: float = Field(..., description="Total operating expenses.")
    cost_And_Expenses: float = Field(..., description="Total costs and expenses.")
    interest_Income: float = Field(..., description="Interest income.")
    interest_Expense: float = Field(..., description="Interest expense.")
    depreciation_And_Amortization: float = Field(..., description="Depreciation and amortization.")
    ebitda: float = Field(..., description="Earnings Before Interest, Taxes, Depreciation, and Amortization.")
    # ebitdaratio: float = Field(..., description="EBITDA ratio.")
    operating_Income: float = Field(..., description="Operating income.")
    # operatingIncomeRatio: float = Field(..., description="Operating income ratio.")
    total_Other_Income_Expenses_Net: float = Field(..., description="Net total other income/expenses.")
    income_Before_Tax: float = Field(..., description="Income before tax.")
    # incomeBeforeTaxRatio: float = Field(..., description="Income before tax ratio.")
    income_Tax_Expense: float = Field(..., description="Income tax expense.")
    net_Income: float = Field(..., description="Net income.")
    # netIncomeRatio: float = Field(..., description="Net income ratio.")
    eps: float = Field(..., description="Earnings per share.")
    eps_diluted: float = Field(..., description="Diluted earnings per share.")
    weightedAverageShsOut: int = Field(..., description="Weighted average shares outstanding.")
    weightedAverageShsOutDil: int = Field(..., description="Diluted weighted average shares outstanding.")
    link: Optional[str] = Field(None, description="Link to the original filing.")
    finalLink: Optional[str] = Field(None, description="Final link to the filing.")

    @field_validator('report_date', 'filing_Date', mode='before')
    @classmethod
    def parse_date(cls, v):
        if isinstance(v, str) and v:
            try:
                return datetime.strptime(v, '%Y-%m-%d').date()
            except ValueError:
                return None
        return v
    
    @field_validator('accepted_Date', mode='before')
    @classmethod
    def parse_accepted_date(cls, v):
        if isinstance(v, str) and v:
            try:
                return datetime.strptime(v[:19], '%Y-%m-%d %H:%M:%S')
            except ValueError:
                return None
        return v

    model_config = ConfigDict(
        alias_generator=to_camel,
        from_attributes=True,
        populate_by_name=True,
    )

class BalanceSheetStatement(BaseModel):
    report_date: date = Field(..., alias='date', description="Date of the balance sheet.")
    symbol: str = Field(..., description="Stock symbol.")
    cashAndCashEquivalents: float = Field(..., description="Cash and cash equivalents.")
    shortTermInvestments: float = Field(..., description="Short-term investments.")
    netReceivables: float = Field(..., description="Net receivables.")
    inventory: float = Field(..., description="Inventory.")
    totalCurrentAssets: float = Field(..., description="Total current assets.")
    propertyPlantEquipmentNet: float = Field(..., description="Net property, plant, and equipment.")
    goodwillAndIntangibleAssets: float = Field(..., description="Goodwill and intangible assets.")
    totalAssets: float = Field(..., description="Total assets.")
    accountPayables: float = Field(..., description="Accounts payable.")
    shortTermDebt: float = Field(..., description="Short-term debt.")
    totalCurrentLiabilities: float = Field(..., description="Total current liabilities.")
    longTermDebt: float = Field(..., description="Long-term debt.")
    totalLiabilities: float = Field(..., description="Total liabilities.")
    totalStockholdersEquity: float = Field(..., description="Total stockholders' equity.")
    totalLiabilitiesAndStockholdersEquity: float = Field(..., description="Total liabilities and stockholders' equity.")

    @field_validator('report_date', mode='before')
    @classmethod
    def parse_date(cls, v):
        if isinstance(v, str) and v:
            return datetime.strptime(v, '%Y-%m-%d').date()
        return v
    
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )

class CashFlowStatement(BaseModel):
    report_date: date = Field(..., alias='date', description="Date of the cash flow statement.")
    symbol: str = Field(..., description="Stock symbol.")
    netIncome: float = Field(..., description="Net income.")
    depreciationAndAmortization: float = Field(..., description="Depreciation and amortization.")
    deferredIncomeTax: float = Field(..., description="Deferred income tax.")
    stockBasedCompensation: float = Field(..., description="Stock-based compensation.")
    changeInWorkingCapital: float = Field(..., description="Change in working capital.")
    accountsReceivables: float = Field(..., description="Accounts receivables.")
    inventory: float = Field(..., description="Inventory.")
    accountsPayables: float = Field(..., description="Accounts payables.")
    otherWorkingCapital: float = Field(..., description="Other working capital.")
    otherNonCashItems: float = Field(..., description="Other non-cash items.")
    netCashProvidedByOperatingActivities: float = Field(..., description="Net cash from operating activities.")
    investmentsInPropertyPlantAndEquipment: float = Field(..., description="Investments in PP&E.")
    acquisitionsNet: float = Field(..., description="Net acquisitions.")
    purchasesOfInvestments: float = Field(..., description="Purchases of investments.")
    salesMaturitiesOfInvestments: float = Field(..., description="Sales and maturities of investments.")
    otherInvestingActivites: float = Field(..., description="Other investing activities.")
    netCashUsedForInvestingActivites: float = Field(..., description="Net cash used for investing activities.")
    debtRepayment: float = Field(..., description="Debt repayment.")
    commonStockIssued: float = Field(..., description="Common stock issued.")
    commonStockRepurchased: float = Field(..., description="Common stock repurchased.")
    dividendsPaid: float = Field(..., description="Dividends paid.")
    otherFinancingActivites: float = Field(..., description="Other financing activities.")
    netCashUsedProvidedByFinancingActivities: float = Field(..., description="Net cash from financing activities.")
    effectOfForexChangesOnCash: float = Field(..., description="Effect of foreign exchange on cash.")
    netChangeInCash: float = Field(..., description="Net change in cash.")
    cashAtEndOfPeriod: float = Field(..., description="Cash at end of period.")
    cashAtBeginningOfPeriod: float = Field(..., description="Cash at beginning of period.")
    operatingCashFlow: float = Field(..., description="Operating cash flow.")
    capitalExpenditure: float = Field(..., description="Capital expenditure.")
    freeCashFlow: float = Field(..., description="Free cash flow.")

    @field_validator('report_date', mode='before')
    @classmethod
    def parse_date(cls, v):
        if isinstance(v, str) and v:
            return datetime.strptime(v, '%Y-%m-%d').date()
        return v
    
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )

class RevenueSegment(BaseModel):
    report_date: date = Field(..., alias='date', description="Date of the segment data.")
    symbol: str = Field(..., description="Stock symbol.")
    segmentName: str = Field(..., description="Name of the business segment.")
    segmentRevenue: float = Field(..., description="Revenue for the segment.")

    @field_validator('report_date', mode='before')
    @classmethod
    def parse_date(cls, v):
        if isinstance(v, str) and v:
            return datetime.strptime(v, '%Y-%m-%d').date()
        return v
    
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )

class FMPArticle(BaseModel):
    title: str = Field(..., description="Title of the article.")
    publishedDate: datetime = Field(..., description="Publication date and time.")
    author: str = Field(..., description="Author of the article.")
    url: str = Field(..., description="URL to the full article.")
    snippet: str = Field(..., description="A short snippet or summary of the article.")
    source: str = Field(..., description="Source of the article (e.g., 'Financial Modeling Prep').")
    tags: Optional[List[str]] = Field(None, description="List of tags associated with the article.")
    
    @field_validator('publishedDate', mode='before')
    @classmethod
    def parse_published_date(cls, v):
        if isinstance(v, str) and v:
            return datetime.strptime(v[:19], '%Y-%m-%d %H:%M:%S')
        return v
    
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )