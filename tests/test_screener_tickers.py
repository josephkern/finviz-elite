"""Offline tests for the screener() tickers= kwarg — patches _get_url."""

import pytest

import finviz_elite as fe
from finviz_elite import FilterSector, ScreenerColumn, ScreenerRange


@pytest.fixture
def capture_url(monkeypatch):
    """Patch _get_url to capture the constructed URL instead of calling Finviz."""
    captured = {}
    monkeypatch.setenv("AUTH_TOKEN_FINVIZ", "test-token")
    monkeypatch.setattr(
        "finviz_elite._core._get_url",
        lambda url: captured.setdefault("url", url) or "",
    )
    return captured


def test_screener_tickers_list(capture_url):
    fe.screener(tickers=["MSFT", "AAPL", "GOOG"])
    assert "&t=MSFT,AAPL,GOOG" in capture_url["url"]


def test_screener_tickers_str(capture_url):
    fe.screener(tickers="MSFT")
    assert "&t=MSFT" in capture_url["url"]


def test_screener_tickers_with_filters(capture_url):
    fe.screener(
        tickers=["MSFT", "AAPL"],
        filters=[FilterSector.TECHNOLOGY],
        ranges={ScreenerRange.PE: (10, 20)},
    )
    url = capture_url["url"]
    assert "&f=sec_technology,fa_pe_10to20" in url
    assert "&t=MSFT,AAPL" in url


def test_screener_tickers_with_columns(capture_url):
    fe.screener(
        tickers=["MSFT"],
        columns=[ScreenerColumn.TICKER, ScreenerColumn.PRICE],
    )
    url = capture_url["url"]
    assert "&c=1,65" in url
    assert "&t=MSFT" in url


def test_screener_tickers_omitted(capture_url):
    fe.screener()
    assert "&t=" not in capture_url["url"]


def test_screener_tickers_empty_list_omitted(capture_url):
    fe.screener(tickers=[])
    assert "&t=" not in capture_url["url"]


def test_screener_silently_drops_cash_sentinel(capture_url):
    # '$CASH' is a documented portfolio-export sentinel — drop it silently
    # and proceed with the remaining tickers, so portfolio_tickers chains
    # straight into screener.
    fe.screener(tickers=["$CASH", "MSFT", "AAPL"])
    url = capture_url["url"]
    assert "&t=MSFT,AAPL" in url
    assert "$CASH" not in url
    assert "CASH" not in url.split("&t=")[1].split("&")[0]


def test_screener_silently_drops_any_dollar_prefix(capture_url):
    # Any '$'-prefixed token (not just $CASH) is dropped — Finviz would
    # silently strip the '$' and match the bare symbol, returning a row
    # for a different stock. Drop them quietly so a mixed list still
    # screens the equity tickers.
    fe.screener(tickers=["$FOO", "MSFT", "$BAR", "AAPL"])
    url = capture_url["url"]
    assert "&t=MSFT,AAPL" in url
    assert "$" not in url.split("&t=")[1].split("&")[0]


def test_screener_raises_when_only_cash_passed(capture_url):
    # All-dropped list filters down to nothing — refuse rather than
    # fall through to an unrestricted whole-market scan.
    with pytest.raises(ValueError, match=r"nothing left to screen"):
        fe.screener(tickers=["$CASH"])
    assert "url" not in capture_url


def test_screener_raises_when_only_cash_passed_as_string(capture_url):
    with pytest.raises(ValueError, match=r"nothing left to screen"):
        fe.screener(tickers="$CASH")


def test_screener_raises_when_all_dollar_prefixed(capture_url):
    # Mix of $CASH and other $-prefixed — still filters to empty.
    with pytest.raises(ValueError, match=r"nothing left to screen"):
        fe.screener(tickers=["$CASH", "$FOO", "$BAR"])
    assert "url" not in capture_url
