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
