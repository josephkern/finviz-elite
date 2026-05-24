"""FastMCP server exposing the six finviz_elite endpoints as MCP tools.

Filter members are passed as dotted strings (``"FilterSector.TECHNOLOGY"``)
to keep the schema compact. Use ``list_filter_classes`` and ``list_enum``
for discovery.
"""

from typing import Dict, List, Optional

import finviz_elite as fe
from mcp.server.fastmcp import FastMCP

from ._resolve import (
    list_enum as _list_enum,
    list_filter_classes as _list_filter_classes,
    resolve_filters,
    resolve_member,
    resolve_members,
    resolve_ranges,
)
from ._throttle import gate


mcp = FastMCP("finviz-elite")


_ENUMS_BY_NAME = {
    "FilingFilter": fe.FilingFilter,
    "FilingOrder": fe.FilingOrder,
    "GroupBy": fe.GroupBy,
    "GroupColumn": fe.GroupColumn,
    "GroupOrder": fe.GroupOrder,
    "NewsFeed": fe.NewsFeed,
    "OptionsType": fe.OptionsType,
    "PortfolioColumn": fe.PortfolioColumn,
    "PortfolioOrder": fe.PortfolioOrder,
    "QuotePeriod": fe.QuotePeriod,
    "QuoteRange": fe.QuoteRange,
    "ScreenerColumn": fe.ScreenerColumn,
    "ScreenerOrder": fe.ScreenerOrder,
    "ScreenerRange": fe.ScreenerRange,
}


@mcp.tool()
def screener(
    filters: Optional[List[str]] = None,
    ranges: Optional[Dict[str, List[Optional[float]]]] = None,
    tickers: Optional[List[str]] = None,
    columns: Optional[List[str]] = None,
    order: Optional[str] = None,
    descending: bool = False,
    raw_filters: Optional[List[str]] = None,
) -> str:
    """Run the Finviz stock screener; returns CSV.

    Args:
        filters: Dotted filter specs like "FilterSector.TECHNOLOGY". Use
            list_filter_classes() to discover available classes/members.
        ranges: Custom numeric ranges keyed by ScreenerRange member name,
            e.g. {"PE": [10, 20]}. Either bound may be null for open-ended.
            Use list_enum("ScreenerRange") to discover members.
        tickers: Optional ticker list, e.g. ["MSFT", "AAPL", "GOOG"].
            Restricts the export to the named symbols.
        columns: ScreenerColumn member names, e.g. ["TICKER", "MARKET_CAP"].
        order: ScreenerOrder member name, e.g. "MARKET_CAP".
        descending: Sort descending. Requires `order`.
        raw_filters: Escape hatch — raw Finviz f= tokens, used verbatim.
    """
    gate.wait()
    return fe.screener(
        filters=resolve_filters(filters),
        ranges=resolve_ranges(ranges),
        tickers=list(tickers) if tickers else None,
        columns=resolve_members(fe.ScreenerColumn, columns),
        order=resolve_member(fe.ScreenerOrder, order),
        descending=descending,
        raw_filters=list(raw_filters) if raw_filters else None,
    )


@mcp.tool()
def options(
    ticker: str,
    expiration: Optional[str] = None,
    strike: Optional[float] = None,
    type: str = "OPTIONS_CHAIN",
) -> str:
    """Download an options chain as CSV.

    Args:
        ticker: Stock symbol, e.g. "MSFT".
        expiration: Optional ISO date ("YYYY-MM-DD") for a single expiration.
            Must match a listed expiration; arbitrary dates return a header-
            only CSV. Omit to span every expiration (can exceed 3,000 rows).
        strike: Optional strike price (e.g. 420.0) to filter to one strike
            across all (or filtered) expirations.
        type: OptionsType member name. Defaults to "OPTIONS_CHAIN".
    """
    gate.wait()
    return fe.options(
        ticker=ticker,
        expiration=expiration,
        strike=strike,
        type=resolve_member(fe.OptionsType, type) or fe.OptionsType.OPTIONS_CHAIN,
    )


@mcp.tool()
def quote(
    ticker: str,
    range: Optional[str] = None,
    period: str = "DAILY",
) -> str:
    """Download OHLCV bars for a ticker; returns CSV.

    Args:
        ticker: Stock symbol, e.g. "MSFT".
        range: QuoteRange member name (e.g. "Y1"). Omit for Finviz default.
        period: QuotePeriod member name. Defaults to "DAILY".
    """
    gate.wait()
    return fe.quote(
        ticker=ticker,
        range=resolve_member(fe.QuoteRange, range),
        period=resolve_member(fe.QuotePeriod, period) or fe.QuotePeriod.DAILY,
    )


@mcp.tool()
def news(feed: str, tickers: Optional[List[str]] = None) -> str:
    """Download a Finviz news feed; returns CSV.

    Args:
        feed: NewsFeed member name, e.g. "STOCKS" or "MARKET_BY_TIME".
        tickers: Optional ticker filter; only valid for ticker-based feeds
            (STOCKS, ETFS, CRYPTO).
    """
    gate.wait()
    return fe.news(
        feed=resolve_member(fe.NewsFeed, feed),  # type: ignore[arg-type]
        tickers=list(tickers) if tickers else None,
    )


@mcp.tool()
def groups(
    by: str,
    columns: Optional[List[str]] = None,
    order: Optional[str] = None,
    descending: bool = False,
) -> str:
    """Download group statistics (sector/industry/country/cap) as CSV.

    Args:
        by: GroupBy member name, e.g. "SECTOR" or "INDUSTRY".
        columns: GroupColumn member names.
        order: GroupOrder member name.
        descending: Sort descending. Requires `order`.
    """
    gate.wait()
    return fe.groups(
        by=resolve_member(fe.GroupBy, by),  # type: ignore[arg-type]
        columns=resolve_members(fe.GroupColumn, columns),
        order=resolve_member(fe.GroupOrder, order),
        descending=descending,
    )


@mcp.tool()
def portfolio(
    pid: int,
    columns: Optional[List[str]] = None,
    order: Optional[str] = None,
    descending: bool = False,
) -> str:
    """Download a Finviz portfolio as CSV.

    Args:
        pid: Portfolio id (read from the portfolio URL: portfolio.ashx?pid=XXX).
        columns: PortfolioColumn member names.
        order: PortfolioOrder member name.
        descending: Sort descending. Requires `order`.
    """
    gate.wait()
    return fe.portfolio(
        pid=pid,
        columns=resolve_members(fe.PortfolioColumn, columns),
        order=resolve_member(fe.PortfolioOrder, order),
        descending=descending,
    )


@mcp.tool()
def portfolio_tickers(pid: int) -> List[str]:
    """Return the distinct tickers in a Finviz portfolio, in portfolio order.

    Lot duplicates are collapsed. $CASH positions are included as-is.
    The result can be passed directly to screener(tickers=...), which
    silently drops any $-prefixed token (Finviz would otherwise strip
    the $ and match the bare symbol, e.g. $CASH -> ticker CASH,
    Pathward Financial Inc).

    Args:
        pid: Portfolio id (read from the portfolio URL: portfolio.ashx?pid=XXX).
    """
    gate.wait()
    return fe.portfolio_tickers(pid=pid)


@mcp.tool()
def filings(
    ticker: str,
    filter: Optional[str] = None,
    order: Optional[str] = None,
    descending: bool = False,
) -> str:
    """Download a ticker's latest SEC filings as CSV.

    Args:
        ticker: Stock symbol, e.g. "MSFT".
        filter: FilingFilter member name, e.g. "ANNUAL_QUARTERLY_CURRENT".
        order: FilingOrder member name.
        descending: Sort descending. Requires `order`.
    """
    gate.wait()
    return fe.filings(
        ticker=ticker,
        filter=resolve_member(fe.FilingFilter, filter),
        order=resolve_member(fe.FilingOrder, order),
        descending=descending,
    )


@mcp.tool()
def list_filter_classes() -> Dict[str, List[str]]:
    """List every FilterXxx class and its members (for the screener `filters` arg)."""
    return _list_filter_classes()


@mcp.tool()
def list_enum(enum_name: str) -> List[str]:
    """List members of a finviz_elite enum by class name.

    Valid names: FilingFilter, FilingOrder, GroupBy, GroupColumn, GroupOrder,
    NewsFeed, OptionsType, PortfolioColumn, PortfolioOrder, QuotePeriod,
    QuoteRange, ScreenerColumn, ScreenerOrder, ScreenerRange.
    """
    cls = _ENUMS_BY_NAME.get(enum_name)
    if cls is None:
        valid = ", ".join(sorted(_ENUMS_BY_NAME))
        raise ValueError(f"Unknown enum {enum_name!r}. Valid: {valid}")
    return _list_enum(cls)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
