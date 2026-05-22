import requests
import os

from dotenv import load_dotenv

load_dotenv()

FINVIZ_URL_BASE = "https://elite.finviz.com"
AUTH_TOKEN_ENV_VAR = "AUTH_TOKEN_FINVIZ"


def _buildURL(base_url: str, data_url: str, options_url: str) -> str:
    """Build a complete URL with authentication token."""
    auth_token = os.getenv(AUTH_TOKEN_ENV_VAR)
    if not auth_token:
        raise ValueError(f"{AUTH_TOKEN_ENV_VAR} not found in environment variables")

    return f"{base_url}/{data_url}?{options_url}&auth={auth_token}"

def _getURL(url: str) -> str:
    """Fetch URL and return response text. Raises exceptions on error."""
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def news(type: str) -> str:
    """
    Download News for a given type.

    Example Arguments:
    Market news
        "v=1" - Ordered by time
        "v=2" - Ordered by source
        "c=1" - News only (optional)
        "c=2" - Blogs only (optional)
    Stocks news
        "v=3" - Stocks feed (no-ETFs)
        "v=4" - ETFs feed
        "pid=12345" - Portfolio news
        "t=MSFT,AAPL" - Filter out only for specified tickers (optional)
    Crypto news
        "v=5" - Crypto feed
        "t=BTC,ETH" - Filter out only for specified tickers (optional)

    Example: https://elite.finviz.com/news_export?v=1
    """
    return pass


def quote(ticker: str, range: str = '') -> str:
    """
    Download OHLVC data for a given ticker.

    Example Arguments:
        ticker: 'MSFT'
        range: d1, d5, m1, m3, m6, ytd, y1, y2, y5, max

    Example: https://elite.finviz.com/quote_export?t=MSFT&p=d&r=d1&auth=token
    """

    data = "quote_export"
    options = f"t={ticker}&p=d"
    if range:
        options += f"&r={range}"
    url = _buildURL(FINVIZ_URL_BASE, data, options)
    return _getURL(url)
