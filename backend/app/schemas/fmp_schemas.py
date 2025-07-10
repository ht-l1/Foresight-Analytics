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
    fiscal_Year: str = Field(..., description="The fiscal year of the report.")
    period: str = Field(..., description="The reporting period (e.g., 'Q1', 'FY').")
    cash_And_Cash_Equivalents: float = Field(..., description="Cash and cash equivalents.")
    short_Term_Investments: float = Field(..., description="Short-term investments.")
    net_Receivables: float = Field(..., description="Net receivables.")
    inventory: float = Field(..., description="Inventory.")
    total_Current_Assets: float = Field(..., description="Total current assets.")
    property_Plant_Equipment_Net: float = Field(..., description="Net property, plant, and equipment.")
    goodwill_And_Intangible_Assets: float = Field(..., description="Goodwill and intangible assets.")
    total_Assets: float = Field(..., description="Total assets.")
    account_Payables: float = Field(..., description="Accounts payable.")
    short_Term_Debt: float = Field(..., description="Short-term debt.")
    total_Current_Liabilities: float = Field(..., description="Total current liabilities.")
    long_Term_Debt: float = Field(..., description="Long-term debt.")
    total_Liabilities: float = Field(..., description="Total liabilities.")
    total_Stockholders_Equity: float = Field(..., description="Total stockholders' equity.")
    total_Liabilities_And_Stockholders_Equity: Optional[float] = Field(None,
    description="Total liabilities and stockholders' equity.")

    @field_validator('report_date', mode='before')
    @classmethod
    def parse_date(cls, v):
        if isinstance(v, str) and v:
            return datetime.strptime(v, '%Y-%m-%d').date()
        return v
    
    model_config = ConfigDict(
        alias_generator=to_camel,
        from_attributes=True,
        populate_by_name=True,
    )

class CashFlowStatement(BaseModel):
    report_date: date = Field(..., alias='date', description="Date of the cash flow statement.")
    fiscal_Year: str = Field(..., alias="fiscalYear", description="The fiscal year of the report.")
    period: str = Field(..., description="The reporting period (e.g., 'Q1', 'FY').")
    symbol: str = Field(..., description="Stock symbol.")
    reported_currency: str = Field(..., alias='reportedCurrency', description="Reported currency.")
    cik: str = Field(..., description="CIK identifier.")
    filing_date: date = Field(..., alias='filingDate', description="Filing date.")
    accepted_date: datetime = Field(..., alias='acceptedDate', description="Accepted date/time.")

    net_Income: float = Field(..., alias="netIncome", description="Net income.")
    depreciation_And_Amortization: float = Field(..., alias="depreciationAndAmortization", description="Depreciation and amortization.")
    deferred_Income_Tax: float = Field(..., alias="deferredIncomeTax", description="Deferred income tax.")
    stock_Based_Compensation: float = Field(..., alias="stockBasedCompensation", description="Stock-based compensation.")
    change_In_Working_Capital: float = Field(..., alias="changeInWorkingCapital", description="Change in working capital.")
    accounts_Receivables: float = Field(..., alias="accountsReceivables", description="Accounts receivables.")
    inventory: float = Field(..., description="Inventory.")
    accounts_Payables: float = Field(..., alias="accountsPayables", description="Accounts payables.")
    other_Working_Capital: float = Field(..., alias="otherWorkingCapital", description="Other working capital.")
    other_Non_Cash_Items: float = Field(..., alias="otherNonCashItems", description="Other non-cash items.")

    net_Cash_Provided_By_Operating_Activities: float = Field(..., alias="netCashProvidedByOperatingActivities", description="Net cash from operating activities.")
    investments_In_Property_Plant_And_Equipment: float = Field(..., alias="investmentsInPropertyPlantAndEquipment", description="Investments in PP&E.")
    acquisitions_Net: float = Field(..., alias="acquisitionsNet", description="Net acquisitions.")
    purchases_Of_Investments: float = Field(..., alias="purchasesOfInvestments", description="Purchases of investments.")
    sales_Maturities_Of_Investments: float = Field(..., alias="salesMaturitiesOfInvestments", description="Sales and maturities of investments.")
    other_Investing_Activities: float = Field(..., alias="otherInvestingActivities", description="Other investing activities.")
    net_Cash_Used_For_Investing_Activities: float = Field(..., alias="netCashProvidedByInvestingActivities", description="Net cash from investing activities.")

    debt_Repayment: float = Field(..., alias="netDebtIssuance", description="Net debt issuance (repayment if negative).")
    long_term_net_debt_issuance: float = Field(..., alias="longTermNetDebtIssuance", description="Long-term net debt issuance.")
    short_term_net_debt_issuance: float = Field(..., alias="shortTermNetDebtIssuance", description="Short-term net debt issuance.")

    net_stock_issuance: float = Field(..., alias="netStockIssuance", description="Net stock issuance.")
    net_common_stock_issuance: float = Field(..., alias="netCommonStockIssuance", description="Net common stock issuance.")
    common_stock_issuance: float = Field(..., alias="commonStockIssuance", description="Common stock issuance.")
    common_Stock_Repurchased: float = Field(..., alias="commonStockRepurchased", description="Common stock repurchased.")

    net_preferred_stock_issuance: float = Field(..., alias="netPreferredStockIssuance", description="Net preferred stock issuance.")
    net_dividends_paid: float = Field(..., alias="netDividendsPaid", description="Net dividends paid.")
    dividends_Paid: float = Field(..., alias="commonDividendsPaid", description="Common dividends paid.")
    preferred_dividends_paid: float = Field(..., alias="preferredDividendsPaid", description="Preferred dividends paid.")
    other_Financing_Activities: float = Field(..., alias="otherFinancingActivities", description="Other financing activities.")
    net_Cash_Used_Provided_By_Financing_Activities: float = Field(..., alias="netCashProvidedByFinancingActivities", description="Net cash from financing activities.")

    effect_Of_Forex_Changes_On_Cash: float = Field(..., alias="effectOfForexChangesOnCash", description="Effect of foreign exchange on cash.")
    net_Change_In_Cash: float = Field(..., alias="netChangeInCash", description="Net change in cash.")
    cash_At_End_Of_Period: float = Field(..., alias="cashAtEndOfPeriod", description="Cash at end of period.")
    cash_At_Beginning_Of_Period: float = Field(..., alias="cashAtBeginningOfPeriod", description="Cash at beginning of period.")

    operating_Cash_Flow: float = Field(..., alias="operatingCashFlow", description="Operating cash flow.")
    capital_Expenditure: float = Field(..., alias="capitalExpenditure", description="Capital expenditure.")
    free_Cash_Flow: float = Field(..., alias="freeCashFlow", description="Free cash flow.")

    income_taxes_paid: float = Field(..., alias="incomeTaxesPaid", description="Income taxes paid.")
    interest_paid: float = Field(..., alias="interestPaid", description="Interest paid.")

    @field_validator('report_date', mode='before')
    @classmethod
    def parse_date(cls, v):
        if isinstance(v, str) and v:
            return datetime.strptime(v, '%Y-%m-%d').date()
        return v
    
    model_config = ConfigDict(
        alias_generator=to_camel,
        from_attributes=True,
        populate_by_name=True,
    )

class RevenueSegment(BaseModel):
    report_date: date = Field(..., alias='date', 
    description="Date of the segment data.")
    fiscal_Year: str = Field(..., description="The fiscal year of the report.")
    period: str = Field(..., description="The reporting period (e.g., 'Q1', 'FY').")
    symbol: str = Field(..., description="Stock symbol.")
    segment_Name: str = Field(..., description="Name of the business segment.")
    segment_Revenue: float = Field(..., description="Revenue for the segment.")

    @field_validator('report_date', mode='before')
    @classmethod
    def parse_date(cls, v):
        if isinstance(v, str) and v:
            return datetime.strptime(v, '%Y-%m-%d').date()
        return v
    
    model_config = ConfigDict(
        alias_generator=to_camel,
        from_attributes=True,
        populate_by_name=True,
    )

class FMPArticle(BaseModel):
    title: str
    published_Date: datetime = Field(alias="date")
    author: str
    url: str = Field(alias="link")
    snippet: str = Field(alias="content")
    source: str = Field(alias="site")
    tickers: str
    image: Optional[str] = None
    
    @field_validator('published_Date', mode='before')
    @classmethod
    def parse_published_date(cls, v):
        if isinstance(v, str) and v:
            return datetime.strptime(v[:19], '%Y-%m-%d %H:%M:%S')
        return v
    
    model_config = ConfigDict(
        alias_generator=to_camel,
        from_attributes=True,
        populate_by_name=True,
    )

class KeyMetrics(BaseModel):
    symbol: str = Field(..., description="The stock symbol of the company.")
    date: str = Field(..., description="The date of the financial report.")
    fiscal_year: str = Field(..., alias="fiscalYear", description="The fiscal year of the report.")
    period: str = Field(..., description="The reporting period (e.g., 'FY' for fiscal year, 'Q1' for first quarter).")
    reported_currency: str = Field(..., alias="reportedCurrency", description="The currency in which the report is filed.")
    market_cap: float = Field(..., alias="marketCap", description="The total market value of the company's outstanding shares.")
    enterprise_value: float = Field(..., alias="enterpriseValue", description="A measure of a company's total value.")
    ev_to_sales: float = Field(..., alias="evToSales", description="Enterprise Value to Sales ratio.")
    ev_to_operating_cash_flow: float = Field(..., alias="evToOperatingCashFlow", description="Enterprise Value to Operating Cash Flow ratio.")
    ev_to_free_cash_flow: float = Field(..., alias="evToFreeCashFlow", description="Enterprise Value to Free Cash Flow ratio.")
    ev_to_ebitda: float = Field(..., alias="evToEBITDA", description="Enterprise Value to EBITDA ratio.")
    net_debt_to_ebitda: float = Field(..., alias="netDebtToEBITDA", description="Net Debt to EBITDA ratio.")
    current_ratio: float = Field(..., alias="currentRatio", description="Measures a company's ability to pay short-term obligations.")
    income_quality: float = Field(..., alias="incomeQuality", description="Ratio of operating cash flow to net income.")
    graham_number: float = Field(..., alias="grahamNumber", description="A theoretical intrinsic value of a stock.")
    working_capital: float = Field(..., alias="workingCapital", description="The difference between current assets and current liabilities.")
    invested_capital: float = Field(..., alias="investedCapital", description="The total amount of money raised by a company by issuing securities.")
    return_on_assets: float = Field(..., alias="returnOnAssets", description="Indicator of how profitable a company is relative to its total assets.")
    return_on_equity: float = Field(..., alias="returnOnEquity", description="The amount of net income returned as a percentage of shareholders equity.")
    return_on_invested_capital: float = Field(..., alias="returnOnInvestedCapital", description="Measures the return that an investment generates for those who have provided capital.")
    earnings_yield: float = Field(..., alias="earningsYield", description="The earnings per share for the most recent 12-month period divided by the current market price per share.")
    free_cash_flow_yield: float = Field(..., alias="freeCashFlowYield", description="A company's free cash flow per share divided by its market price per share.")
    capex_to_operating_cash_flow: float = Field(..., alias="capexToOperatingCashFlow", description="Capital Expenditures to Operating Cash Flow ratio.")
    capex_to_revenue: float = Field(..., alias="capexToRevenue", description="Capital Expenditures to Revenue ratio.")
    research_and_developement_to_revenue: float = Field(..., alias="researchAndDevelopementToRevenue", description="R&D to Revenue ratio.")
    stock_based_compensation_to_revenue: float = Field(..., alias="stockBasedCompensationToRevenue", description="Stock-Based Compensation to Revenue ratio.")
    days_of_sales_outstanding: float = Field(..., alias="daysOfSalesOutstanding", description="Average number of days that it takes a company to collect payment for a sale.")
    days_of_payables_outstanding: float = Field(..., alias="daysOfPayablesOutstanding", description="Average number of days a company takes to pay its suppliers.")
    days_of_inventory_outstanding: float = Field(..., alias="daysOfInventoryOutstanding", description="Average number of days a company holds its inventory before selling it.")
    operating_cycle: float = Field(..., alias="operatingCycle", description="The time it takes a company to receive inventory, sell it, and collect cash.")
    cash_conversion_cycle: float = Field(..., alias="cashConversionCycle", description="The time it takes for a company to convert its investments in inventory and other resources into cash.")

    @field_validator('date', mode='before')
    @classmethod
    def parse_published_date(cls, v):
        if isinstance(v, str) and v:
            return datetime.strptime(v[:19], '%Y-%m-%d %H:%M:%S')
        return v

    model_config = ConfigDict(
        alias_generator=to_camel,
        from_attributes=True,
        populate_by_name=True,
    )


class FinancialRatios(BaseModel):
    symbol: str = Field(..., description="The stock symbol of the company.")
    date: str = Field(..., description="The date of the financial report.")
    fiscal_year: str = Field(..., alias="fiscalYear", description="The fiscal year of the report.")
    period: str = Field(..., description="The reporting period (e.g., 'FY').")
    gross_profit_margin: float = Field(..., alias="grossProfitMargin", description="Gross profit as a percentage of revenue.")
    net_profit_margin: float = Field(..., alias="netProfitMargin", description="Net profit as a percentage of revenue.")
    receivables_turnover: float = Field(..., alias="receivablesTurnover", description="How efficiently a company uses its assets.")
    inventory_turnover: float = Field(..., alias="inventoryTurnover", description="Shows how many times a company has sold and replaced inventory during a given period.")
    asset_turnover: float = Field(..., alias="assetTurnover", description="The ratio of total sales or revenue to average assets.")
    current_ratio: float = Field(..., alias="currentRatio", description="Measures a company's ability to pay short-term obligations.")
    quick_ratio: float = Field(..., alias="quickRatio", description="Measures a company's ability to meet its short-term obligations with its most liquid assets.")
    price_to_earnings_ratio: float = Field(..., alias="priceToEarningsRatio", description="The ratio for valuing a company that measures its current share price relative to its per-share earnings.")
    price_to_book_ratio: float = Field(..., alias="priceToBookRatio", description="Compares a company's market capitalization to its book value.")
    price_to_sales_ratio: float = Field(..., alias="priceToSalesRatio", description="Compares a company's stock price to its revenue.")
    price_to_free_cash_flow_ratio: float = Field(..., alias="priceToFreeCashFlowRatio", description="Compares a company's market capitalization to its free cash flow.")
    debt_to_equity_ratio: float = Field(..., alias="debtToEquityRatio", description="Total debt and financial liabilities against shareholders' equity.")
    dividend_payout_ratio: float = Field(..., alias="dividendPayoutRatio", description="The proportion of earnings paid out as dividends to shareholders.")
    dividend_yield: float = Field(..., alias="dividendYield", description="A financial ratio that shows how much a company pays out in dividends each year relative to its stock price.")
    return_on_equity: float = Field(..., alias="returnOnEquity", description="The amount of net income returned as a percentage of shareholders equity.")
    revenue_per_share: float = Field(..., alias="revenuePerShare", description="Total revenue divided by the number of shares outstanding.")
    net_income_per_share: float = Field(..., alias="netIncomePerShare", description="Net income divided by the number of shares outstanding.")
    operating_cash_flow_per_share: float = Field(..., alias="operatingCashFlowPerShare", description="Operating cash flow divided by the number of shares outstanding.")
    free_cash_flow_per_share: float = Field(..., alias="freeCashFlowPerShare", description="Free cash flow divided by the number of shares outstanding.")
    effective_tax_rate: float = Field(..., alias="effectiveTaxRate", description="The percent of its income that an individual or a corporation pays in taxes.")

    @field_validator('date', mode='before')
    @classmethod
    def parse_published_date(cls, v):
        if isinstance(v, str) and v:
            return datetime.strptime(v[:19], '%Y-%m-%d %H:%M:%S')
        return v

    model_config = ConfigDict(
        alias_generator=to_camel,
        from_attributes=True,
        populate_by_name=True,
    )


class KeyMetricsTTM(BaseModel):
    symbol: str = Field(..., description="The stock symbol of the company.")
    market_cap: float = Field(..., alias="marketCap", description="The total market value of the company's outstanding shares.")
    enterprise_value_ttm: float = Field(..., alias="enterpriseValueTTM", description="A measure of a company's total value (TTM).")
    ev_to_sales_ttm: float = Field(..., alias="evToSalesTTM", description="Enterprise Value to Sales ratio (TTM).")
    ev_to_free_cash_flow_ttm: float = Field(..., alias="evToFreeCashFlowTTM", description="Enterprise Value to Free Cash Flow ratio (TTM).")
    ev_to_ebitda_ttm: float = Field(..., alias="evToEBITDATTM", description="Enterprise Value to EBITDA ratio (TTM).")
    net_debt_to_ebitda_ttm: float = Field(..., alias="netDebtToEBITDATTM", description="Net Debt to EBITDA ratio (TTM).")
    current_ratio_ttm: float = Field(..., alias="currentRatioTTM", description="Measures ability to pay short-term obligations (TTM).")
    return_on_equity_ttm: float = Field(..., alias="returnOnEquityTTM", description="Net income as a percentage of shareholders equity (TTM).")
    earnings_yield_ttm: float = Field(..., alias="earningsYieldTTM", description="Earnings per share relative to market price (TTM).")
    free_cash_flow_yield_ttm: float = Field(..., alias="freeCashFlowYieldTTM", description="Free cash flow per share relative to market price (TTM).")
    capex_to_revenue_ttm: float = Field(..., alias="capexToRevenueTTM", description="Capital Expenditures to Revenue ratio (TTM).")
    research_and_developement_to_revenue_ttm: float = Field(..., alias="researchAndDevelopementToRevenueTTM", description="R&D to Revenue ratio (TTM).")
    cash_conversion_cycle_ttm: float = Field(..., alias="cashConversionCycleTTM", description="Time to convert investments into cash (TTM).")

    @field_validator('*', mode='before')
    @classmethod
    def parse_published_date(cls, v):
        if isinstance(v, str) and v:
            return datetime.strptime(v[:19], '%Y-%m-%d %H:%M:%S')
        return v

    model_config = ConfigDict(
        alias_generator=to_camel,
        from_attributes=True,
        populate_by_name=True,
    )


class FinancialRatiosTTM(BaseModel):
    symbol: str = Field(..., description="The stock symbol of the company.")
    gross_profit_margin_ttm: float = Field(..., alias="grossProfitMarginTTM", description="Gross profit as a percentage of revenue (TTM).")
    net_profit_margin_ttm: float = Field(..., alias="netProfitMarginTTM", description="Net profit as a percentage of revenue (TTM).")
    asset_turnover_ttm: float = Field(..., alias="assetTurnoverTTM", description="Ratio of total sales to average assets (TTM).")
    current_ratio_ttm: float = Field(..., alias="currentRatioTTM", description="Measures ability to pay short-term obligations (TTM).")
    price_to_earnings_ratio_ttm: float = Field(..., alias="priceToEarningsRatioTTM", description="Share price relative to per-share earnings (TTM).")
    price_to_sales_ratio_ttm: float = Field(..., alias="priceToSalesRatioTTM", description="Compares stock price to revenue (TTM).")
    price_to_free_cash_flow_ratio_ttm: float = Field(..., alias="priceToFreeCashFlowRatioTTM", description="Market cap to free cash flow (TTM).")
    debt_to_equity_ratio_ttm: float = Field(..., alias="debtToEquityRatioTTM", description="Total debt against shareholders' equity (TTM).")
    dividend_payout_ratio_ttm: float = Field(..., alias="dividendPayoutRatioTTM", description="Proportion of earnings paid as dividends (TTM).")
    dividend_yield_ttm: float = Field(..., alias="dividendYieldTTM", description="Annual dividend per share as a percentage of the stock's price (TTM).")
    return_on_equity_ttm: float = Field(..., alias="returnOnEquityTTM", description="Net income as a percentage of shareholders equity (TTM).")
    net_income_per_share_ttm: float = Field(..., alias="netIncomePerShareTTM", description="Net income per share (TTM).")
    free_cash_flow_per_share_ttm: float = Field(..., alias="freeCashFlowPerShareTTM", description="Free cash flow per share (TTM).")
    effective_tax_rate_ttm: float = Field(..., alias="effectiveTaxRateTTM", description="The percent of income a corporation pays in taxes (TTM).")
    enterprise_value_ttm: float = Field(..., alias="enterpriseValueTTM", description="A measure of a company's total value (TTM).")

    @field_validator('*', mode='before')
    @classmethod
    def parse_published_date(cls, v):
        if isinstance(v, str) and v:
            return datetime.strptime(v[:19], '%Y-%m-%d %H:%M:%S')
        return v

    model_config = ConfigDict(
        alias_generator=to_camel,
        from_attributes=True,
        populate_by_name=True,
    )
