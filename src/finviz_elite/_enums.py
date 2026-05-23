"""Enumerations describing the Finviz Elite export endpoints.

This module is the "vocabulary" of the package -- the fixed value sets
that the export endpoints accept (feed types, time ranges, column
indices, sort keys). It has no dependencies on the rest of the package
so it can be imported anywhere without risk of a circular import.
"""

from enum import Enum


class NewsFeed(Enum):
    """Finviz news feeds, mapped to their ``v=`` query value.

    Ticker filtering is only meaningful for the ticker-based feeds
    (STOCKS, ETFS, CRYPTO). The market feeds (MARKET_BY_TIME,
    MARKET_BY_SOURCE) are not associated with tickers -- see
    ``TICKER_FEEDS`` and ``news()``.
    """

    MARKET_BY_TIME = "1"    # Market news, ordered by time
    MARKET_BY_SOURCE = "2"  # Market news, ordered by source
    STOCKS = "3"            # Stocks feed (no ETFs)
    ETFS = "4"              # ETFs feed
    CRYPTO = "5"            # Crypto feed


# Feeds for which the ``t=`` ticker filter is supported. The market
# feeds carry no ticker column, so Finviz silently ignores ``t=`` there.
TICKER_FEEDS = frozenset({NewsFeed.STOCKS, NewsFeed.ETFS, NewsFeed.CRYPTO})


class QuoteRange(Enum):
    """Time range for a quote export, mapped to its ``r=`` query value."""

    D1 = "d1"     # 1 day
    D5 = "d5"     # 5 days
    M1 = "m1"     # 1 month
    M3 = "m3"     # 3 months
    M6 = "m6"     # 6 months
    YTD = "ytd"   # year to date
    Y1 = "y1"     # 1 year
    Y2 = "y2"     # 2 years
    Y5 = "y5"     # 5 years
    MAX = "max"   # all available history


class QuotePeriod(Enum):
    """Bar periodicity for a quote export, mapped to its ``p=`` query value.

    Values verified against the live quote_export endpoint. Intraday
    bars (MIN_*, HOURLY) carry a time component in the Date column;
    DAILY/WEEKLY/MONTHLY carry a date only. Note Finviz has no 60-minute
    intraday code -- use HOURLY ("h") instead.
    """

    MIN_1 = "i1"
    MIN_2 = "i2"
    MIN_3 = "i3"
    MIN_5 = "i5"
    MIN_10 = "i10"
    MIN_15 = "i15"
    MIN_30 = "i30"
    HOURLY = "h"
    DAILY = "d"
    WEEKLY = "w"
    MONTHLY = "m"


class FilingFilter(Enum):
    """SEC filing categories for the latest-filings export, mapped to
    their ``f=`` query value.

    When omitted from ``filings()`` the export returns all filing
    types. An unrecognised ``f=`` value is silently ignored, so passing
    a real FilingFilter member is the only way to guarantee a filter.
    """

    ANNUAL_QUARTERLY_CURRENT = "annual-quarterly-current"
    INSIDER_EQUITY = "insider-equity"
    BENEFICIAL_OWNERSHIP = "beneficial-ownership"
    EXEMPT_OFFERINGS = "exempt-offerings"
    REGISTRATION_STATEMENTS = "registration-statements"
    FILING_REVIEW_CORRESPONDENCE = "filing-review-correspondence"
    SEC_ORDERS_NOTICES = "sec-orders-notices"
    PROXY_MATERIALS = "proxy-materials"
    TENDER_OFFERS = "tender-offers"
    TRUST_INDENTURES = "trust-indentures"


class FilingOrder(Enum):
    """Sortable columns for the latest-filings export, mapped to their
    ``o=`` query value.
    """

    FILING_DATE = "filingDate"
    REPORT_DATE = "reportDate"
    FORM = "form"


class GroupBy(Enum):
    """Finviz group type, mapped to its ``g=`` query value.

    Selects how stocks are aggregated for the groups export.
    """

    SECTOR = "sector"
    INDUSTRY = "industry"
    COUNTRY = "country"
    CAPITALIZATION = "capitalization"


class GroupColumn(Enum):
    """Group export columns, mapped to their ``c=`` index.

    Used to subset and order the exported columns. Indices and labels
    match the live grp_export header (custom view, v=152).
    """

    NO = 0
    NAME = 1
    MARKET_CAP = 2
    PE = 3
    FORWARD_PE = 4
    PEG = 5
    PS = 6
    PB = 7
    PC = 8
    P_FREE_CASH_FLOW = 9
    DIVIDEND_YIELD = 10
    EPS_GROWTH_PAST_5Y = 11
    EPS_GROWTH_NEXT_5Y = 12
    SALES_GROWTH_PAST_5Y = 13
    FLOAT_SHORT = 14
    PERF_WEEK = 15
    PERF_MONTH = 16
    PERF_QUARTER = 17
    PERF_HALF_YEAR = 18
    PERF_YEAR = 19
    PERF_YTD = 20
    ANALYST_RECOM = 21
    AVG_VOLUME = 22
    RELATIVE_VOLUME = 23
    CHANGE = 24
    VOLUME = 25
    STOCKS = 26


class GroupOrder(Enum):
    """Sortable group columns, mapped to their ``o=`` name token.

    Every token is verified against the live grp_export endpoint.
    Member names mirror GroupColumn (minus NO, the row index, which
    is not a meaningful sort key). An unrecognised ``o=`` value is
    silently ignored, so passing a real GroupOrder member is the only
    way to guarantee a sort.
    """

    NAME = "name"
    MARKET_CAP = "marketcap"
    PE = "pe"
    FORWARD_PE = "forwardpe"
    PEG = "peg"
    PS = "ps"
    PB = "pb"
    PC = "pc"
    P_FREE_CASH_FLOW = "pfcf"
    DIVIDEND_YIELD = "dividendyield"
    EPS_GROWTH_PAST_5Y = "eps5years"
    EPS_GROWTH_NEXT_5Y = "estltgrowth"
    SALES_GROWTH_PAST_5Y = "sales5years"
    FLOAT_SHORT = "shortinterestshare"
    PERF_WEEK = "perf1w"
    PERF_MONTH = "perf4w"
    PERF_QUARTER = "perf13w"
    PERF_HALF_YEAR = "perf26w"
    PERF_YEAR = "perf52w"
    PERF_YTD = "perfytd"
    ANALYST_RECOM = "recom"
    AVG_VOLUME = "averagevolume"
    RELATIVE_VOLUME = "relativevolume"
    CHANGE = "change"
    VOLUME = "volume"
    STOCKS = "count"


class PortfolioColumn(Enum):
    """Portfolio export columns, mapped to their ``c=`` index.

    Used to subset and order the exported columns. The index values
    and labels match the live portfolio_export header.
    """

    TICKER = 0
    COMPANY = 1
    PRICE = 2
    CHANGE_PCT = 3       # Change%
    VOLUME = 4
    TRANSACTION = 5
    DATE = 6
    SHARES = 7
    COST = 8
    MARKET_VALUE = 9
    GAIN_DOLLAR = 10     # Gain$
    GAIN_PCT = 11        # Gain%
    CHANGE_DOLLAR = 12   # Change$


class PortfolioOrder(Enum):
    """Sortable portfolio columns, mapped to their ``o=`` name.

    The ``o=`` value names are verified against the live
    portfolio_export endpoint. GAIN_DOLLAR and CHANGE_DOLLAR are
    intentionally absent: that endpoint does not support ordering by
    the Gain$ / Change$ columns (it silently ignores the request).
    An unrecognised ``o=`` value is likewise ignored, so passing a
    real PortfolioOrder member is the only way to guarantee a sort.
    """

    TICKER = "ticker"
    COMPANY = "company"
    PRICE = "price"
    CHANGE_PCT = "changepct"
    VOLUME = "volume"
    TRANSACTION = "transaction"
    DATE = "date"
    SHARES = "shares"
    COST = "cost"
    MARKET_VALUE = "marketvalue"
    GAIN_PCT = "gainpct"


class ScreenerColumn(Enum):
    """Screener export columns, mapped to their ``c=`` index.

    Used to subset and reorder the exported columns. Indices and labels
    match the Finviz screener custom view (v=152). Columns 90-99 are
    intraday performance; 100-124 are ETF-specific fields.
    """

    NO = 0
    TICKER = 1
    COMPANY = 2
    SECTOR = 3
    INDUSTRY = 4
    COUNTRY = 5
    MARKET_CAP = 6
    PE = 7
    FORWARD_PE = 8
    PEG = 9
    PS = 10
    PB = 11
    P_CASH = 12
    P_FREE_CASH_FLOW = 13
    DIVIDEND_YIELD = 14
    PAYOUT_RATIO = 15
    EPS_TTM = 16
    EPS_GROWTH_THIS_YEAR = 17
    EPS_GROWTH_NEXT_YEAR = 18
    EPS_GROWTH_PAST_5Y = 19
    EPS_GROWTH_NEXT_5Y = 20
    SALES_GROWTH_PAST_5Y = 21
    EPS_GROWTH_QOQ = 22
    SALES_GROWTH_QOQ = 23
    SHARES_OUTSTANDING = 24
    SHARES_FLOAT = 25
    INSIDER_OWNERSHIP = 26
    INSIDER_TRANSACTIONS = 27
    INSTITUTIONAL_OWNERSHIP = 28
    INSTITUTIONAL_TRANSACTIONS = 29
    SHORT_FLOAT = 30
    SHORT_RATIO = 31
    RETURN_ON_ASSETS = 32
    RETURN_ON_EQUITY = 33
    RETURN_ON_INVESTED_CAPITAL = 34
    CURRENT_RATIO = 35
    QUICK_RATIO = 36
    LT_DEBT_EQUITY = 37
    TOTAL_DEBT_EQUITY = 38
    GROSS_MARGIN = 39
    OPERATING_MARGIN = 40
    PROFIT_MARGIN = 41
    PERF_WEEK = 42
    PERF_MONTH = 43
    PERF_QUARTER = 44
    PERF_HALF_YEAR = 45
    PERF_YEAR = 46
    PERF_YTD = 47
    BETA = 48
    AVERAGE_TRUE_RANGE = 49
    VOLATILITY_WEEK = 50
    VOLATILITY_MONTH = 51
    SMA_20 = 52
    SMA_50 = 53
    SMA_200 = 54
    HIGH_50D = 55
    LOW_50D = 56
    HIGH_52W = 57
    LOW_52W = 58
    RSI_14 = 59
    CHANGE_FROM_OPEN = 60
    GAP = 61
    ANALYST_RECOM = 62
    AVERAGE_VOLUME = 63
    RELATIVE_VOLUME = 64
    PRICE = 65
    CHANGE = 66
    VOLUME = 67
    EARNINGS_DATE = 68
    TARGET_PRICE = 69
    IPO_DATE = 70
    AFTER_HOURS_CLOSE = 71
    AFTER_HOURS_CHANGE = 72
    BOOK_PER_SH = 73
    CASH_PER_SH = 74
    DIVIDEND = 75
    EMPLOYEES = 76
    EPS_NEXT_Q = 77
    INCOME = 78
    INDEX = 79
    OPTIONABLE = 80
    PREV_CLOSE = 81
    SALES = 82
    SHORTABLE = 83
    SHORT_INTEREST = 84
    FLOAT_PCT = 85
    OPEN = 86
    HIGH = 87
    LOW = 88
    TRADES = 89
    PERF_1MIN = 90
    PERF_2MIN = 91
    PERF_3MIN = 92
    PERF_5MIN = 93
    PERF_10MIN = 94
    PERF_15MIN = 95
    PERF_30MIN = 96
    PERF_1H = 97
    PERF_2H = 98
    PERF_4H = 99
    ASSET_TYPE = 100
    ETF_TYPE = 101
    REGION = 102
    SINGLE_CATEGORY = 103
    SECTOR_THEME = 104
    TAGS = 105
    ACTIVE_PASSIVE = 106
    NET_EXPENSE_RATIO = 107
    TOTAL_HOLDINGS = 108
    ASSETS_UNDER_MANAGEMENT = 109
    NET_ASSET_VALUE = 110
    NET_ASSET_VALUE_PCT = 111
    NET_FLOWS_1M = 112
    NET_FLOWS_PCT_1M = 113
    NET_FLOWS_3M = 114
    NET_FLOWS_PCT_3M = 115
    NET_FLOWS_YTD = 116
    NET_FLOWS_PCT_YTD = 117
    NET_FLOWS_1Y = 118
    NET_FLOWS_PCT_1Y = 119
    RETURN_1Y = 120
    RETURN_3Y = 121
    RETURN_5Y = 122
    RETURN_10Y = 123
    RETURN_SINCE_INCEPTION = 124
    ALL_TIME_HIGH = 125
    ALL_TIME_LOW = 126
    EPS_SURPRISE = 127
    REVENUE_SURPRISE = 128
    EXCHANGE = 129
    DIVIDEND_TTM = 130
    DIVIDEND_EX_DATE = 131
    EPS_YOY_TTM = 132
    SALES_YOY_TTM = 133
    RANGE_52W = 134
    NEWS_TIME = 135
    NEWS_URL = 136
    NEWS_TITLE = 137
    PERF_3Y = 138
    PERF_5Y = 139
    PERF_10Y = 140
    AFTER_HOURS_VOLUME = 141
    EPS_GROWTH_PAST_3Y = 142
    SALES_GROWTH_PAST_3Y = 143
    ENTERPRISE_VALUE = 144
    EV_EBITDA = 145
    EV_SALES = 146
    DIVIDEND_GROWTH_1Y = 147
    DIVIDEND_GROWTH_3Y = 148
    DIVIDEND_GROWTH_5Y = 149
    DAILY_DIGEST = 150


class ScreenerOrder(Enum):
    """Sortable screener columns, mapped to their ``o=`` name token.

    Member names mirror ScreenerColumn. This is a curated subset of the
    151 screener columns: the commonly-sorted ones whose ``o=`` token
    was verified against the live screener export (or shares the token
    namespace verified for the groups export). Columns with no useful
    sort (news fields, ETF metadata, etc.) are intentionally omitted.
    An unrecognised ``o=`` value is silently ignored by Finviz, so
    passing a real ScreenerOrder member is the only way to guarantee
    a sort.
    """

    TICKER = "ticker"
    COMPANY = "company"
    SECTOR = "sector"
    INDUSTRY = "industry"
    COUNTRY = "country"
    MARKET_CAP = "marketcap"
    PE = "pe"
    FORWARD_PE = "forwardpe"
    PEG = "peg"
    PS = "ps"
    PB = "pb"
    P_CASH = "pc"
    P_FREE_CASH_FLOW = "pfcf"
    DIVIDEND_YIELD = "dividendyield"
    PAYOUT_RATIO = "payoutratio"
    EPS_TTM = "eps"
    EPS_GROWTH_THIS_YEAR = "epsyoy"
    EPS_GROWTH_PAST_5Y = "eps5years"
    EPS_GROWTH_NEXT_5Y = "estltgrowth"
    SALES_GROWTH_PAST_5Y = "sales5years"
    INSIDER_OWNERSHIP = "insiderown"
    INSTITUTIONAL_OWNERSHIP = "instown"
    SHORT_FLOAT = "shortinterestshare"
    RETURN_ON_ASSETS = "roa"
    RETURN_ON_EQUITY = "roe"
    RETURN_ON_INVESTED_CAPITAL = "roi"
    LT_DEBT_EQUITY = "ltdebteq"
    GROSS_MARGIN = "grossmargin"
    OPERATING_MARGIN = "opermargin"
    PROFIT_MARGIN = "netmargin"
    PERF_WEEK = "perf1w"
    PERF_MONTH = "perf4w"
    PERF_QUARTER = "perf13w"
    PERF_HALF_YEAR = "perf26w"
    PERF_YEAR = "perf52w"
    PERF_YTD = "perfytd"
    PERF_3Y = "perf3y"
    BETA = "beta"
    SMA_20 = "sma20"
    SMA_50 = "sma50"
    SMA_200 = "sma200"
    GAP = "gap"
    ANALYST_RECOM = "recom"
    AVERAGE_VOLUME = "averagevolume"
    RELATIVE_VOLUME = "relativevolume"
    PRICE = "price"
    CHANGE = "change"
    VOLUME = "volume"
    TARGET_PRICE = "targetprice"
