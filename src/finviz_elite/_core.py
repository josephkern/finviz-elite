import requests
import os

from enum import Enum
from typing import List, Optional, Union

from dotenv import load_dotenv

from ._enums import (
    FilingFilter,
    FilingOrder,
    GroupBy,
    GroupColumn,
    GroupOrder,
    NewsFeed,
    PortfolioColumn,
    PortfolioOrder,
    QuotePeriod,
    QuoteRange,
    ScreenerColumn,
    ScreenerOrder,
    TICKER_FEEDS,
)

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


def filings(
    ticker: str,
    filter: Optional[FilingFilter] = None,
    order: Optional[FilingOrder] = None,
    descending: bool = False,
) -> str:
    """
    Download a stock's latest SEC filings as CSV.

    Arguments:
        ticker: stock symbol, e.g. "MSFT".
        filter: optional filing category, a FilingFilter member (e.g.
            FilingFilter.ANNUAL_QUARTERLY_CURRENT). When omitted, all
            filing types are returned.
        order: optional column to sort by, a FilingOrder member.
            When omitted, Finviz returns its default order.
        descending: sort descending instead of ascending. Only has an
            effect when 'order' is given; passing it alone raises
            ValueError.

    Examples:
        filings("MSFT")
        filings("MSFT", filter=FilingFilter.PROXY_MATERIALS)
        filings("MSFT", order=FilingOrder.FILING_DATE, descending=True)

    Example URL: https://elite.finviz.com/export/latest-filings?t=MSFT&o=-filingDate
    """
    if descending and order is None:
        raise ValueError("descending=True requires an 'order' to sort by.")

    data = "export/latest-filings"
    options = f"t={ticker}"
    if filter:
        options += f"&f={filter.value}"
    if order:
        options += f"&o={'-' if descending else ''}{order.value}"

    url = _build_url(FINVIZ_URL_BASE, data, options)
    return _get_url(url)

def groups(
    by: GroupBy,
    columns: Optional[List[GroupColumn]] = None,
    order: Optional[GroupOrder] = None,
    descending: bool = False,
) -> str:
    """
    Download Finviz group statistics as CSV.

    Groups aggregate the whole market by sector, industry, country or
    market-cap band, with averaged valuation/performance metrics.

    Arguments:
        by: which grouping to pull, a GroupBy member.
        columns: optional subset of columns to export, as a list of
            GroupColumn members. The export follows the given order.
            When omitted, Finviz returns its default column set.
        order: optional column to sort by, a GroupOrder member.
            When omitted, Finviz returns its default order.
        descending: sort descending instead of ascending. Only has an
            effect when 'order' is given; passing it alone raises
            ValueError.

    Examples:
        groups(GroupBy.SECTOR)
        groups(GroupBy.INDUSTRY, columns=[GroupColumn.NAME,
                                          GroupColumn.MARKET_CAP])
        groups(GroupBy.SECTOR, order=GroupOrder.MARKET_CAP, descending=True)

    Example URL: https://elite.finviz.com/grp_export?g=sector&v=152&c=0,1,2
    """
    if descending and order is None:
        raise ValueError("descending=True requires an 'order' to sort by.")

    # v=152 is the custom-columns view; it is what makes c= take effect.
    data = "grp_export"
    options = f"g={by.value}&v=152"
    if columns:
        options += "&c=" + ",".join(str(col.value) for col in columns)
    if order:
        options += f"&o={'-' if descending else ''}{order.value}"

    url = _build_url(FINVIZ_URL_BASE, data, options)
    return _get_url(url)


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


def screener(
    filters: Optional[List[Union[str, Enum]]] = None,
    columns: Optional[List[ScreenerColumn]] = None,
    order: Optional[ScreenerOrder] = None,
    descending: bool = False,
) -> str:
    """
    Run the Finviz stock screener and download the result as CSV.

    Arguments:
        filters: optional screening criteria, a list of filter tokens.
            Each item may be a filter enum member (FilterSector,
            FilterExchange, FilterIndex, FilterMarketCap) or a raw
            Finviz token string for the long tail of filters not
            covered by an enum (e.g. "fa_div_pos"). When omitted, the
            whole market is returned.
        columns: optional subset of columns to export, as a list of
            ScreenerColumn members. The export follows the given order.
            When omitted, Finviz returns its default column set.
        order: optional column to sort by, a ScreenerOrder member.
            When omitted, Finviz returns its default order.
        descending: sort descending instead of ascending. Only has an
            effect when 'order' is given; passing it alone raises
            ValueError.

    Examples:
        screener(filters=[FilterSector.TECHNOLOGY, FilterMarketCap.LARGE])
        screener(filters=["fa_div_pos", FilterSector.TECHNOLOGY],
                 columns=[ScreenerColumn.TICKER, ScreenerColumn.PRICE])
        screener(order=ScreenerOrder.MARKET_CAP, descending=True)

    Example URL: https://elite.finviz.com/export?v=152&c=0,1,2&f=sec_technology
    """
    if descending and order is None:
        raise ValueError("descending=True requires an 'order' to sort by.")

    # v=152 is the custom-columns view; it is what makes c= take effect.
    data = "export"
    options = "v=152"
    if columns:
        options += "&c=" + ",".join(str(col.value) for col in columns)
    if filters:
        tokens = [f.value if isinstance(f, Enum) else str(f) for f in filters]
        options += "&f=" + ",".join(tokens)
    if order:
        options += f"&o={'-' if descending else ''}{order.value}"

    url = _build_url(FINVIZ_URL_BASE, data, options)
    return _get_url(url)
