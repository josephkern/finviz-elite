import csv
import os
from io import StringIO
from typing import Dict, List, Optional, Tuple, Union

import requests
from dotenv import load_dotenv

from ._enums import (
    FilingFilter,
    FilingOrder,
    GroupBy,
    GroupColumn,
    GroupOrder,
    NewsFeed,
    OptionsType,
    PortfolioColumn,
    PortfolioOrder,
    QuotePeriod,
    QuoteRange,
    ScreenerColumn,
    ScreenerOrder,
    TICKER_FEEDS,
)
from ._filters import FilterEnum, ScreenerRange

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
    response = requests.get(url, timeout=30)
    if response.status_code == 429:
        raise RuntimeError(
            "Finviz rate-limited (HTTP 429). Increase the throttle interval "
            "with FINVIZ_MCP_MIN_INTERVAL_S=<seconds> (default 13)."
        )
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


def options(
    ticker: str,
    expiration: Optional[str] = None,
    strike: Optional[float] = None,
    type: OptionsType = OptionsType.OPTIONS_CHAIN,
) -> str:
    """
    Download an options chain as CSV.

    Arguments:
        ticker: stock symbol, e.g. "MSFT".
        expiration: optional ISO date ("YYYY-MM-DD") to filter to a
            single expiration. Must match a listed expiration -- an
            arbitrary date returns a header-only CSV. Omit to span
            every expiration (large for liquid names: a single pull
            for an active mega-cap can exceed 3,000 contracts).
        strike: optional strike price to filter to a single strike
            (e.g. 420.0). Returns every contract at that strike
            across all expirations (or the one filtered above).
        type: OptionsType member; defaults to OPTIONS_CHAIN.

    Column note: the result schema is *dynamic*. The unfiltered chain
    returns 18 columns including ``Expiry`` and ``Strike``. Filtering
    by ``expiration`` drops the ``Expiry`` column; filtering by
    ``strike`` drops the ``Strike`` column. Filtering by both drops
    both. Greeks (Delta/Gamma/Theta/Vega/Rho) and IV are always
    included and are computed server-side. Contract names follow OCC
    format (e.g. ``MSFT260618P00175000``).

    Examples:
        options("MSFT")
        options("MSFT", expiration="2026-06-19")
        options("MSFT", strike=420.0)
        options("MSFT", expiration="2026-06-19", strike=420.0)

    Example URL: https://elite.finviz.com/export/options?t=MSFT&ty=oc&e=2026-06-19
    """
    data = "export/options"
    opts = f"t={ticker}&ty={type.value}"
    if expiration:
        opts += f"&e={expiration}"
    if strike is not None:
        opts += f"&s={strike:g}"

    url = _build_url(FINVIZ_URL_BASE, data, opts)
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


def portfolio_tickers(pid: Union[int, str]) -> List[str]:
    """
    Return the distinct tickers from a Finviz portfolio, in portfolio order.

    Portfolios track separate lots as separate rows, so the same ticker
    can appear several times; duplicates are collapsed via first-
    occurrence order. Cash positions (``$CASH``) are real portfolio
    entries and are included in the result.

    The output can be fed directly to ``screener(tickers=...)`` or
    ``news(tickers=...)`` -- screener silently drops the ``$CASH``
    sentinel (and raises on any other ``$``-prefixed token, which
    would otherwise be silently substituted server-side):

        screener(tickers=portfolio_tickers(pid),
                 filters=[FilterSector.TECHNOLOGY])

    Arguments:
        pid: portfolio id, same as portfolio(). Read from the portfolio
            URL (.../portfolio.ashx?pid=XXXXXXX).

    Rate-limit note: this is one HTTP request. When chained with another
    Finviz call, the 13s spacing between requests still applies.
    """
    csv_text = portfolio(pid, columns=[PortfolioColumn.TICKER])
    reader = csv.DictReader(StringIO(csv_text))
    tickers = [row["Ticker"] for row in reader if row.get("Ticker")]
    return list(dict.fromkeys(tickers))


def _build_range_token(
    metric: ScreenerRange,
    minimum: Optional[float],
    maximum: Optional[float],
) -> Optional[str]:
    """Build the ``f=`` token for a Finviz Elite custom numeric range.

    Returns ``None`` when both bounds are ``None`` -- Finviz silently
    rejects the open-on-both-sides form ``{prefix}_to`` and would just
    return the unfiltered universe.

    HighLow/AllTime metrics embed a direction suffix in their enum
    value via a ``|`` separator (e.g. ``ta_highlow52w|-bhx``); the
    suffix is appended *after* the bounds, producing tokens like
    ``ta_highlow52w_10to30-bhx``.
    """
    if minimum is None and maximum is None:
        return None
    lo = "" if minimum is None else f"{minimum:g}"
    hi = "" if maximum is None else f"{maximum:g}"
    spec = metric.value
    suffix = ""
    if "|" in spec:
        spec, suffix = spec.split("|", 1)
    return f"{spec}_{lo}to{hi}{suffix}"


def screener(
    filters: Optional[List[FilterEnum]] = None,
    ranges: Optional[Dict[ScreenerRange, Tuple[Optional[float], Optional[float]]]] = None,
    tickers: Optional[Union[str, List[str]]] = None,
    columns: Optional[List[ScreenerColumn]] = None,
    order: Optional[ScreenerOrder] = None,
    descending: bool = False,
    raw_filters: Optional[List[str]] = None,
) -> str:
    """
    Run the Finviz stock screener and download the result as CSV.

    Arguments:
        filters: optional screening criteria, a list of filter enum
            members (any member of FilterEnum: FilterExchange,
            FilterIndex, FilterSector, FilterMarketCap, ...). When
            omitted, the whole market is returned.
        ranges: optional Elite custom numeric ranges, a dict keyed by
            ScreenerRange member with ``(min, max)`` tuples as values.
            Either bound may be ``None`` for an open-ended range; both
            ``None`` skips the metric. Example:
            ``ranges={ScreenerRange.PE: (10, 20)}``.
        tickers: optional ticker filter, a single symbol ("AAPL") or a
            list (["MSFT", "AAPL"]). Restricts the export to the named
            symbols. Combines with ``filters``/``ranges``: a row must
            match both the ticker set and any filters applied.
        columns: optional subset of columns to export, as a list of
            ScreenerColumn members. The export follows the given order.
            When omitted, Finviz returns its default column set.
        order: optional column to sort by, a ScreenerOrder member.
            When omitted, Finviz returns its default order.
        descending: sort descending instead of ascending. Only has an
            effect when 'order' is given; passing it alone raises
            ValueError.
        raw_filters: last-resort escape hatch for filter tokens not yet
            modeled as enum members. Strings are appended to ``f=``
            verbatim. Prefer the typed ``filters`` and ``ranges`` params;
            reach for this only when neither covers the filter you need.

    Examples:
        screener(filters=[FilterSector.TECHNOLOGY, FilterMarketCap.LARGE])
        screener(ranges={ScreenerRange.PE: (10, 20)})
        screener(tickers=["MSFT", "AAPL", "GOOG"])
        screener(filters=[FilterSector.TECHNOLOGY],
                 ranges={ScreenerRange.BETA: (None, 1.5)})
        screener(raw_filters=["fa_div_pos"])
        screener(order=ScreenerOrder.MARKET_CAP, descending=True)

    Example URL:
        https://elite.finviz.com/export?v=152&c=0,1,2&f=sec_technology,fa_pe_10to20
        https://elite.finviz.com/export?v=152&t=MSFT,AAPL,GOOG
    """
    if descending and order is None:
        raise ValueError("descending=True requires an 'order' to sort by.")

    # v=152 is the custom-columns view; it is what makes c= take effect.
    data = "export"
    options = "v=152"
    if columns:
        options += "&c=" + ",".join(str(col.value) for col in columns)

    tokens: List[str] = []
    if filters:
        tokens.extend(f.value for f in filters)
    if ranges:
        for metric, (lo, hi) in ranges.items():
            token = _build_range_token(metric, lo, hi)
            if token is not None:
                tokens.append(token)
    if raw_filters:
        tokens.extend(raw_filters)
    if tokens:
        options += "&f=" + ",".join(tokens)

    if tickers:
        if isinstance(tickers, str):
            tickers = [tickers]
        # '$CASH' is a documented Finviz portfolio-export sentinel; the
        # same library produces it via portfolio_tickers(). Drop it
        # silently so chaining portfolio_tickers -> screener Just Works.
        # Any other '$'-prefixed token is unknown territory (typo, future
        # sentinel, user confusion) -- raise rather than letting Finviz
        # silently strip the '$' and substitute a real listed symbol
        # (e.g. '$CASH' -> ticker CASH, Pathward Financial Inc).
        cleaned = []
        for t in tickers:
            if t == "$CASH":
                continue
            if t.startswith("$"):
                raise ValueError(
                    f"Ticker {t!r} is not a valid symbol. Finviz strips "
                    f"the '$' and matches the bare symbol, so this would "
                    f"silently return a row for a different stock. Only "
                    f"the documented '$CASH' portfolio sentinel is "
                    f"dropped automatically; remove other '$'-prefixed "
                    f"entries before calling screener()."
                )
            cleaned.append(t)
        if not cleaned:
            raise ValueError(
                "All tickers were '$CASH' (cash positions); nothing left "
                "to screen. Add equity tickers to the list."
            )
        options += f"&t={','.join(cleaned)}"

    if order:
        options += f"&o={'-' if descending else ''}{order.value}"

    url = _build_url(FINVIZ_URL_BASE, data, options)
    return _get_url(url)
