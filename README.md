# finviz-elite

Python client for the [Finviz Elite](https://elite.finviz.com/) CSV export
endpoints, plus an optional MCP server that exposes the same endpoints as
tools for Claude and other MCP clients.

Requires a Finviz Elite subscription and the auth token attached to your
account. The library wraps seven endpoints — `screener`, `quote`, `news`,
`groups`, `portfolio`, `filings`, `options` — with typed enum surfaces for
every filter, column, and order option.

> This is an unofficial client library for users with their own Finviz Elite
> subscription. Not affiliated with or endorsed by Finviz Financial
> Visualizations, LLC.

## Requirements

- Python 3.10+
- A [Finviz Elite](https://elite.finviz.com/) subscription
- The `auth=` token from your Finviz session (see Authentication below)

## Install

```bash
uv pip install -e .            # core library only
uv pip install -e ".[mcp]"     # core + MCP server
```

## Authentication

Set `AUTH_TOKEN_FINVIZ` in the environment, or drop it into a `.env` file
at the project root (auto-loaded via `python-dotenv`):

```
AUTH_TOKEN_FINVIZ=your-token-here
```

The token is the `auth=` query param Finviz appends to export URLs when
you're signed in.

## Library usage

Every endpoint returns CSV as a string. All filter/column/order args are
enum members, so an IDE will autocomplete the full surface.

```python
import finviz_elite as fe

# Run the screener with typed filters and a custom numeric range
csv = fe.screener(
    filters=[fe.FilterSector.TECHNOLOGY, fe.FilterMarketCap.LARGE],
    ranges={fe.ScreenerRange.PE: (10, 20)},
    order=fe.ScreenerOrder.MARKET_CAP,
    descending=True,
)

# Or restrict the screener to a specific ticker list (e.g. your watchlist
# or portfolio holdings) — composes with filters/ranges
csv = fe.screener(tickers=["MSFT", "AAPL", "GOOG"])

# OHLCV bars
fe.quote("MSFT", range=fe.QuoteRange.Y1, period=fe.QuotePeriod.DAILY)

# Group statistics (sector / industry / country / cap)
fe.groups(fe.GroupBy.SECTOR)

# News feed, optionally filtered to a ticker
fe.news(fe.NewsFeed.STOCKS, tickers=["MSFT", "AAPL"])

# Portfolio export (pid from .../portfolio.ashx?pid=XXX)
fe.portfolio(12345678)

# Distinct tickers from a portfolio (lot duplicates collapsed; $CASH
# is a real position and is included).
positions = fe.portfolio_tickers(12345678)

# Feed straight into screener — any $-prefixed token (including the
# $CASH sentinel) is silently dropped, since Finviz would otherwise
# strip the $ and match the bare symbol (e.g. $CASH → ticker CASH,
# Pathward Financial Inc).
fe.screener(tickers=positions, filters=[fe.FilterSector.TECHNOLOGY])

# Latest SEC filings for a ticker
fe.filings("MSFT", order=fe.FilingOrder.FILING_DATE, descending=True)

# Options chain (omit expiration/strike to span everything — large!)
fe.options("MSFT", expiration="2026-06-19")
fe.options("MSFT", strike=420.0)
```

The screener also takes a `raw_filters` escape hatch for tokens not yet
modeled as enum members — see the docstring on `fe.screener`.

### Filter surface

75 `FilterXxx` enum classes cover the Descriptive / Fundamental /
Technical / ETF tiers of the Finviz screener, plus `ScreenerRange` for
custom numeric ranges (PE, beta, margins, growth rates, etc.). All
members were verified against the live API.

## MCP server

`finviz_elite_mcp` is a sibling package that exposes the six library
endpoints (plus two discovery tools) over MCP/stdio.

### Setup with Claude Code

After installing the MCP extra, create a project-scoped `.mcp.json` in
the directory where you want Claude Code to use the server:

```json
{
  "mcpServers": {
    "finviz-elite": {
      "type": "stdio",
      "command": ".venv/bin/finviz-elite-mcp",
      "args": [],
      "env": {}
    }
  }
}
```

Adjust `command` to match your environment:

- Relative path (`.venv/bin/finviz-elite-mcp`) works when Claude Code
  runs from the project root.
- Use the absolute path (`/abs/path/to/.venv/bin/finviz-elite-mcp`) if
  Claude Code runs from elsewhere.
- Or use `python -m finviz_elite_mcp` if the venv's `python` is on PATH.

Restart Claude Code and approve the project-scoped `finviz-elite`
server when prompted.

### Tools

| Tool | What it does |
| --- | --- |
| `screener` | Run the stock screener; returns CSV |
| `quote` | OHLCV bars for a ticker |
| `news` | News feed (optionally filtered by ticker) |
| `groups` | Sector/industry/country/cap statistics |
| `portfolio` | Export a Finviz portfolio |
| `filings` | Latest SEC filings for a ticker |
| `options` | Options chain (optionally filtered by expiration or strike) |
| `list_filter_classes` | Enumerate every `FilterXxx` class and its members |
| `list_enum` | List members of any non-filter enum (columns, orders, ranges, periods, etc.) |

### Filter convention

MCP clients pass filter members as **dotted strings** that the server
resolves into enum members:

```json
{
  "filters": ["FilterSector.TECHNOLOGY", "FilterMarketCap.LARGE"],
  "ranges": {"PE": [10, 20], "BETA": [null, 1.5]},
  "order": "MARKET_CAP",
  "descending": true
}
```

Column/order/period/range/feed args take bare member names (no class
prefix) since the class is implied by the parameter.

### Throttling

A shared min-interval gate protects against Finviz's burst-sensitive
rate limit (a single 429 poisons the rest of a batch). The default is
13 seconds between hits; override with:

```bash
export FINVIZ_MCP_MIN_INTERVAL_S=20
```

### Running the server directly

```bash
finviz-elite-mcp           # console script
python -m finviz_elite_mcp # module entry
```

Both speak MCP over stdio.

## Development

```bash
uv pip install -e ".[mcp]" pytest
pytest tests/
```

The test suite is offline — no Finviz auth or network needed for the
resolver tests.

## License

MIT — see [LICENSE](LICENSE).
