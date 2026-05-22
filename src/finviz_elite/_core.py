import requests
import os
from dotenv import load_dotenv

load_dotenv()

FINVIZ_URL_BASE = "https://elite.finviz.com"
AUTH_TOKEN_ENV_VAR = "AUTH_TOKEN_FINVIZ"


def _build_url(base_url: str, command_url: str, options_url: str) -> str:
    """Build a complete URL with authentication token."""
    auth_token = os.getenv(AUTH_TOKEN_ENV_VAR)
    if not auth_token:
        raise ValueError(f"{AUTH_TOKEN_ENV_VAR} not found in environment variables")
    return f"{base_url}/{command_url}/?{options_url}&auth={auth_token}"


def quote(ticker: str, period: str) -> str:
    """
    Build quote export URL for a given ticker.

    Example: https://elite.finviz.com/quote_export?t=MSFT&p=d&auth=token
    """
    options = f"t={ticker}&p={period}"
    return _build_url(FINVIZ_URL_BASE, "quote_export", options)
