"""Screener filter enums and the Elite custom-range API.

Split from ``_enums.py`` so that module stays readable as the screener
filter taxonomy fills in -- one enum per filter category, plus the
``ScreenerRange`` enum for the Elite custom numeric-range API and the
``FilterEnum`` union the screener accepts.

Custom-range token shape (verified live against the screener UI):

- Closed:        ``{prefix}_{min}to{max}``    e.g. ``fa_pe_10to20``
- Min only:      ``{prefix}_{min}to``         e.g. ``fa_pe_10to``
- Max only:      ``{prefix}_to{max}``         e.g. ``fa_pe_to20``
- Both ``None``: token omitted -- Finviz rejects ``{prefix}_to``.
"""

from enum import Enum
from typing import Union


class FilterExchange(Enum):
    """Screener exchange filter, mapped to its ``f=`` token."""

    AMEX = "exch_amex"
    NASDAQ = "exch_nasd"
    NYSE = "exch_nyse"


class FilterIndex(Enum):
    """Screener index-membership filter, mapped to its ``f=`` token."""

    SP500 = "idx_sp500"
    DJIA = "idx_dji"
    NASDAQ100 = "idx_ndx"
    RUSSELL2000 = "idx_rut"


class FilterSector(Enum):
    """Screener sector filter, mapped to its ``f=`` token."""

    BASIC_MATERIALS = "sec_basicmaterials"
    COMMUNICATION_SERVICES = "sec_communicationservices"
    CONSUMER_CYCLICAL = "sec_consumercyclical"
    CONSUMER_DEFENSIVE = "sec_consumerdefensive"
    ENERGY = "sec_energy"
    FINANCIAL = "sec_financial"
    HEALTHCARE = "sec_healthcare"
    INDUSTRIALS = "sec_industrials"
    REAL_ESTATE = "sec_realestate"
    TECHNOLOGY = "sec_technology"
    UTILITIES = "sec_utilities"


class FilterMarketCap(Enum):
    """Screener market-cap filter, mapped to its ``f=`` token."""

    MEGA = "cap_mega"     # $200bln and above
    LARGE = "cap_large"   # $10bln to $200bln
    MID = "cap_mid"       # $2bln to $10bln
    SMALL = "cap_small"   # $300mln to $2bln
    MICRO = "cap_micro"   # $50mln to $300mln
    NANO = "cap_nano"     # under $50mln


class ScreenerRange(Enum):
    """Metrics that accept an Elite custom numeric range, mapped to the
    metric's ``f=`` token prefix.

    Bounds are supplied at call time via ``screener(ranges=...)``; the
    token is built as ``{prefix}_{min}to{max}`` with either side omitted
    when ``None``. Both bounds ``None`` skips the metric -- Finviz
    rejects ``{prefix}_to`` outright.
    """

    PE = "fa_pe"
    BETA = "ta_beta"


# Every screener filter enum is a member of this Union. The screener's
# ``filters`` param accepts any member of any enum in this Union, giving
# the MCP surface a single fully-typed pick-from-list.
FilterEnum = Union[
    FilterExchange,
    FilterIndex,
    FilterSector,
    FilterMarketCap,
]
