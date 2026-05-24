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


def test_screener_rejects_dollar_prefixed_ticker(capture_url):
    # Finviz silently substitutes $CASH -> ticker CASH (Pathward Financial Inc).
    # Reject loudly rather than letting silent data corruption through.
    with pytest.raises(ValueError, match=r"\$CASH"):
        fe.screener(tickers=["$CASH", "MSFT"])
    assert "url" not in capture_url  # request must never be built


def test_screener_rejects_any_dollar_prefix(capture_url):
    with pytest.raises(ValueError, match=r"portfolio_tickers"):
        fe.screener(tickers=["$FOO"])
