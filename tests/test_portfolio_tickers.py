"""Offline tests for portfolio_tickers() — patches _get_url."""

import pytest

import finviz_elite as fe


@pytest.fixture
def portfolio_csv(monkeypatch):
    """Factory: install a fake portfolio CSV as the _get_url response."""
    monkeypatch.setenv("AUTH_TOKEN_FINVIZ", "test-token")

    def _install(csv_body: str) -> None:
        monkeypatch.setattr(
            "finviz_elite._core._get_url",
            lambda url: csv_body,
        )

    return _install


# Mirrors the real probe shape: quoted Ticker column, two $CASH rows,
# duplicate ticker rows for separate lots.
SAMPLE_CSV = (
    '"Ticker"\n'
    '"$CASH"\n'
    '"$CASH"\n'
    '"MSFT"\n'
    '"AAPL"\n'
    '"AAPL"\n'
    '"GOOG"\n'
    '"AAPL"\n'
)


def test_dedupes_and_includes_cash(portfolio_csv):
    portfolio_csv(SAMPLE_CSV)
    # $CASH is a real position; dedupe collapses both the cash rows and
    # the duplicate AAPL lots, preserving first-occurrence order.
    assert fe.portfolio_tickers(123) == ["$CASH", "MSFT", "AAPL", "GOOG"]


def test_preserves_first_occurrence_order(portfolio_csv):
    portfolio_csv('"Ticker"\n"ZZZ"\n"AAA"\n"ZZZ"\n"MMM"\n')
    assert fe.portfolio_tickers(123) == ["ZZZ", "AAA", "MMM"]


def test_empty_portfolio(portfolio_csv):
    portfolio_csv('"Ticker"\n')
    assert fe.portfolio_tickers(123) == []


def test_all_cash_portfolio(portfolio_csv):
    portfolio_csv('"Ticker"\n"$CASH"\n"$CASH"\n')
    assert fe.portfolio_tickers(123) == ["$CASH"]


def test_string_pid_accepted(portfolio_csv):
    portfolio_csv('"Ticker"\n"MSFT"\n')
    # portfolio() accepts Union[int, str]; portfolio_tickers must too
    assert fe.portfolio_tickers("12345") == ["MSFT"]
