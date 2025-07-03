from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from decimal import Decimal

class CompanyProfile(BaseModel):
    symbol: str
    companyName: str
    currency: str
    exchange: str
    industry: str
    sector: str
    country: str
    marketCap: Optional[int] = None
    beta: Optional[float] = None
    volAvg: Optional[int] = None
    mktCap: Optional[int] = None
    lastDiv: Optional[float] = None
    range: Optional[str] = None
    changes: Optional[float] = None
    price: Optional[float] = None
    dcfDiff: Optional[float] = None
    dcf: Optional[float] = None
    image: Optional[str] = None
    ipoDate: Optional[date] = None
    defaultImage: Optional[bool] = None
    isEtf: Optional[bool] = None
    isActivelyTrading: Optional[bool] = None
    isAdr: Optional[bool] = None
    isFund: Optional[bool] = None
    description: Optional[str] = None
    ceo: Optional[str] = None
    website: Optional[str] = None
    
    @validator('ipoDate', pre=True)
    def parse_ipo_date(cls, v):
        if isinstance(v, str) and v:
            try:
                return datetime.strptime(v, '%Y-%m-%d').date()
            except ValueError:
                return None
        return v

class IncomeStatement(BaseModel):
    date: date
    symbol: str
    reportedCurrency: str
    cik: Optional[str] = None
    fillingDate: Optional[date] = None
    acceptedDate: Optional[datetime] = None
    calendarYear: str
    period: str
    
    # Revenue & Income
    revenue: Optional[int] = None
    costOfRevenue: Optional[int] = None
    grossProfit: Optional[int] = None
    grossProfitRatio: Optional[float] = None
    
    # Operating
    researchAndDevelopmentExpenses: Optional[int] = None
    generalAndAdministrativeExpenses: Optional[int] = None
    sellingAndMarketingExpenses: Optional[int] = None
    sellingGeneralAndAdministrativeExpenses: Optional[int] = None
    otherExpenses: Optional[int] = None
    operatingExpenses: Optional[int] = None
    costAndExpenses: Optional[int] = None
    interestIncome: Optional[int] = None
    interestExpense: Optional[int] = None
    depreciationAndAmortization: Optional[int] = None
    ebitda: Optional[int] = None
    ebitdaratio: Optional[float] = None
    operatingIncome: Optional[int] = None
    operatingIncomeRatio: Optional[float] = None
    
    # Net Income
    totalOtherIncomeExpensesNet: Optional[int] = None
    incomeBeforeTax: Optional[int] = None
    incomeBeforeTaxRatio: Optional[float] = None
    incomeTaxExpense: Optional[int] = None
    netIncome: Optional[int] = None
    netIncomeRatio: Optional[float] = None
    
    # Per Share
    eps: Optional[float] = None
    epsdiluted: Optional[float] = None
    weightedAverageShsOut: Optional[int] = None
    weightedAverageShsOutDil: Optional[int] = None
    
    # URLs
    link: Optional[str] = None
    finalLink: Optional[str] = None
    
    @validator('date', 'fillingDate', pre=True)
    def parse_date(cls, v):
        if isinstance(v, str) and v:
            try:
                return datetime.strptime(v, '%Y-%m-%d').date()
            except ValueError:
                return None
        return v
    
    @validator('acceptedDate', pre=True)
    def parse_accepted_date(cls, v):
        if isinstance(v, str) and v:
            try:
                return datetime.strptime(v[:19], '%Y-%m-%d %H:%M:%S')
            except ValueError:
                return None
        return v

class BalanceSheet(BaseModel):
    date: date
    symbol: str
    reportedCurrency: str
    cik: Optional[str] = None
    fillingDate: Optional[date] = None
    acceptedDate: Optional[datetime] = None
    calendarYear: str
    period: str
    
    # Assets
    cashAndCashEquivalents: Optional[int] = None
    shortTermInvestments: Optional[int] = None
    cashAndShortTermInvestments: Optional[int] = None
    netReceivables: Optional[int] = None
    inventory: Optional[int] = None
    otherCurrentAssets: Optional[int] = None
    totalCurrentAssets: Optional[int] = None
    propertyPlantEquipmentNet: Optional[int] = None
    goodwill: Optional[int] = None
    intangibleAssets: Optional[int] = None
    goodwillAndIntangibleAssets: Optional[int] = None
    longTermInvestments: Optional[int] = None
    taxAssets: Optional[int] = None
    otherNonCurrentAssets: Optional[int] = None
    totalNonCurrentAssets: Optional[int] = None
    otherAssets: Optional[int] = None
    totalAssets: Optional[int] = None
    
    # Liabilities
    accountPayables: Optional[int] = None
    shortTermDebt: Optional[int] = None
    taxPayables: Optional[int] = None
    deferredRevenue: Optional[int] = None
    otherCurrentLiabilities: Optional[int] = None
    totalCurrentLiabilities: Optional[int] = None
    longTermDebt: Optional[int] = None
    deferredRevenueNonCurrent: Optional[int] = None
    deferredTaxLiabilitiesNonCurrent: Optional[int] = None
    otherNonCurrentLiabilities: Optional[int] = None
    totalNonCurrentLiabilities: Optional[int] = None
    otherLiabilities: Optional[int] = None
    capitalLeaseObligations: Optional[int] = None
    totalLiabilities: Optional[int] = None
    
    # Equity
    preferredStock: Optional[int] = None
    commonStock: Optional[int] = None
    retainedEarnings: Optional[int] = None
    accumulatedOtherComprehensiveIncomeLoss: Optional[int] = None
    othertotalStockholdersEquity: Optional[int] = None
    totalStockholdersEquity: Optional[int] = None
    totalEquity: Optional[int] = None
    totalLiabilitiesAndStockholdersEquity: Optional[int] = None
    minorityInterest: Optional[int] = None
    totalLiabilitiesAndTotalEquity: Optional[int] = None
    
    # Shares
    totalInvestments: Optional[int] = None
    totalDebt: Optional[int] = None
    netDebt: Optional[int] = None
    
    # URLs
    link: Optional[str] = None
    finalLink: Optional[str] = None
    
    @validator('date', 'fillingDate', pre=True)
    def parse_date(cls, v):
        if isinstance(v, str) and v:
            try:
                return datetime.strptime(v, '%Y-%m-%d').date()
            except ValueError:
                return None
        return v
    
    @validator('acceptedDate', pre=True)
    def parse_accepted_date(cls, v):
        if isinstance(v, str) and v:
            try:
                return datetime.strptime(v[:19], '%Y-%m-%d %H:%M:%S')
            except ValueError:
                return None
        return v

class RevenueSegment(BaseModel):
    date: date
    symbol: str
    segment: str
    revenue: int
    
    @validator('date', pre=True)
    def parse_date(cls, v):
        if isinstance(v, str) and v:
            try:
                return datetime.strptime(v, '%Y-%m-%d').date()
            except ValueError:
                return None
        return v

class FMPArticle(BaseModel):
    title: str
    date: datetime
    content: str
    tickers: Optional[str] = None
    image: Optional[str] = None
    link: Optional[str] = None
    author: Optional[str] = None
    site: Optional[str] = None
    
    @validator('date', pre=True)
    def parse_date(cls, v):
        if isinstance(v, str) and v:
            try:
                return datetime.strptime(v, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                return None
        return v