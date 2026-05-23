"""Offline tests for the MCP resolver — no network, no Finviz auth needed."""

import pytest

from finviz_elite import FilterSector, ScreenerRange
from finviz_elite_mcp._resolve import (
    list_filter_classes,
    resolve_filter,
    resolve_filters,
    resolve_member,
    resolve_ranges,
)


def test_resolve_filter_returns_enum_member():
    assert resolve_filter("FilterSector.TECHNOLOGY") is FilterSector.TECHNOLOGY


def test_resolve_filter_unknown_class():
    with pytest.raises(ValueError, match="Unknown filter class"):
        resolve_filter("NotARealClass.FOO")


def test_resolve_filter_unknown_member():
    with pytest.raises(ValueError, match="Unknown FilterSector member"):
        resolve_filter("FilterSector.NOT_A_SECTOR")


def test_resolve_filter_missing_dot():
    with pytest.raises(ValueError, match="must be 'ClassName.MEMBER'"):
        resolve_filter("FilterSector")


def test_resolve_filters_none_returns_none():
    assert resolve_filters(None) is None
    assert resolve_filters([]) is None


def test_resolve_ranges_both_bounds():
    out = resolve_ranges({"PE": [10, 20]})
    assert out == {ScreenerRange.PE: (10.0, 20.0)}


def test_resolve_ranges_open_ended():
    out = resolve_ranges({"BETA": [None, 1.5]})
    assert out == {ScreenerRange.BETA: (None, 1.5)}


def test_resolve_ranges_unknown_metric():
    with pytest.raises(ValueError, match="Unknown ScreenerRange"):
        resolve_ranges({"NOT_A_METRIC": [1, 2]})


def test_resolve_ranges_wrong_arity():
    with pytest.raises(ValueError, match="2-element"):
        resolve_ranges({"PE": [10]})


def test_resolve_member_none_returns_none():
    from finviz_elite import QuoteRange

    assert resolve_member(QuoteRange, None) is None


def test_list_filter_classes_has_known_entries():
    classes = list_filter_classes()
    assert "FilterSector" in classes
    assert "TECHNOLOGY" in classes["FilterSector"]
    # The Union type FilterEnum must not leak through
    assert "FilterEnum" not in classes
