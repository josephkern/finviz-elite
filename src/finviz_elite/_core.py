import requests
import os

from enum import Enum
from typing import List, Optional, Union

from dotenv import load_dotenv

load_dotenv()

FINVIZ_URL_BASE = "https://elite.finviz.com"
AUTH_TOKEN_ENV_VAR = "AUTH_TOKEN_FINVIZ"

def _build_url(base_url: str, data_url: str, options_url: str) -> str:
    """Build a complete URL with authentication token."""
    auth_token = os.getenv(AUTH_TOKEN_ENV_VAR)
    if not auth_token:
        raise ValueError(f"{AUTH_TOKEN_ENV_VAR} not found in environment variables")

    return f"{base_url}/{data_url}?{options_url}&auth={auth_token}"

def _get_url(url: str) -> str:
    """Fetch URL and return response text. Raises exceptions on error."""
    response = requests.get(url)
    response.raise_for_status()
    return response.text

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


def portfolio(
    pid: Union[int, str],
    columns: Optional[List[PortfolioColumn]] = None,
    order: Optional[PortfolioOrder] = None,
    descending: bool = False,
) -> str:
    """
    Download a Finviz portfolio as CSV.

    Arguments:
        pid: the portfolio id. Finviz has no API to list a user's
            portfolios; read the pid from a portfolio's web URL
            (.../portfolio.ashx?pid=XXXXXXX).
        columns: optional subset of columns to export, as a list of
            PortfolioColumn members. The export follows the given
            order. When omitted, all 13 columns are returned.
        order: optional column to sort by, a PortfolioOrder member.
            When omitted, Finviz returns its default order.
        descending: sort descending instead of ascending. Only has an
            effect when 'order' is given; passing it alone raises
            ValueError.

    Examples:
        portfolio(12345678)
        portfolio(12345678, columns=[PortfolioColumn.TICKER,
                                       PortfolioColumn.PRICE])
        portfolio(12345678, order=PortfolioOrder.PRICE, descending=True)

    Example URL: https://elite.finviz.com/portfolio_export?pid=12345&c=0,2&o=-price
    """
    if descending and order is None:
        raise ValueError("descending=True requires an 'order' to sort by.")

    data = "portfolio_export"
    options = f"pid={pid}"
    if columns:
        options += "&c=" + ",".join(str(col.value) for col in columns)
    if order:
        options += f"&o={'-' if descending else ''}{order.value}"

    url = _build_url(FINVIZ_URL_BASE, data, options)
    return _get_url(url)

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


def news(feed: NewsFeed, tickers: Optional[Union[str, List[str]]] = None) -> str:
    """
    Download a Finviz news feed as CSV.

    Arguments:
        feed: which feed to pull, a NewsFeed member. For example
            NewsFeed.STOCKS for stock news or NewsFeed.MARKET_BY_TIME
            for the general market feed.
        tickers: optional ticker filter, a single symbol ("AAPL") or a
            list (["MSFT", "AAPL"]). Only supported for the ticker-based
            feeds (NewsFeed.STOCKS, NewsFeed.ETFS, NewsFeed.CRYPTO);
            passing it for a market feed raises ValueError rather than
            being silently ignored.

    Examples:
        news(NewsFeed.STOCKS, tickers=["MSFT", "AAPL"])
        news(NewsFeed.CRYPTO, tickers="BTC")
        news(NewsFeed.MARKET_BY_TIME)

    Example URL: https://elite.finviz.com/news_export?v=3&t=AAPL
    """
    if tickers and feed not in TICKER_FEEDS:
        raise ValueError(
            f"{feed.name} is a market feed; ticker filtering is not "
            f"supported. Use one of {sorted(f.name for f in TICKER_FEEDS)}."
        )

    data = "news_export"
    options = f"v={feed.value}"
    if tickers:
        if isinstance(tickers, str):
            tickers = [tickers]
        options += f"&t={','.join(tickers)}"

    url = _build_url(FINVIZ_URL_BASE, data, options)
    return _get_url(url)


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


def quote(
    ticker: str,
    range: Optional[QuoteRange] = None,
    period: QuotePeriod = QuotePeriod.DAILY,
) -> str:
    """
    Download OHLCV data for a given ticker as CSV.

    Arguments:
        ticker: stock symbol, e.g. "MSFT".
        range: optional time range, a QuoteRange member (e.g.
            QuoteRange.Y1). When omitted, Finviz returns its default
            range rather than erroring.
        period: bar periodicity, a QuotePeriod member. Defaults to
            QuotePeriod.DAILY.

    Examples:
        quote("MSFT")
        quote("MSFT", range=QuoteRange.Y1)
        quote("AAPL", range=QuoteRange.M6, period=QuotePeriod.WEEKLY)

    Example URL: https://elite.finviz.com/quote_export?t=MSFT&p=d&r=y1
    """
    data = "quote_export"
    options = f"t={ticker}&p={period.value}"
    if range:
        options += f"&r={range.value}"
    url = _build_url(FINVIZ_URL_BASE, data, options)
    return _get_url(url)
