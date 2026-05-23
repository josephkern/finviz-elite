"""Resolve string specs from MCP clients into finviz_elite enum members.

MCP tool inputs are JSON, so callers pass enum members as dotted strings
(``"FilterSector.TECHNOLOGY"``). This module parses those, with clear
errors when a class or member is unknown.
"""

from enum import Enum
from typing import Dict, List, Optional, Sequence, Tuple, Type

import finviz_elite as fe
from finviz_elite import ScreenerRange


def _filter_classes() -> Dict[str, Type[Enum]]:
    """All FilterXxx enum classes exported by finviz_elite (excludes FilterEnum union)."""
    out: Dict[str, Type[Enum]] = {}
    for name in fe.__all__:
        if not name.startswith("Filter") or name == "FilterEnum":
            continue
        obj = getattr(fe, name, None)
        if isinstance(obj, type) and issubclass(obj, Enum):
            out[name] = obj
    return out


_FILTER_CLASSES = _filter_classes()


def resolve_filter(spec: str) -> Enum:
    """Parse ``"FilterSector.TECHNOLOGY"`` into ``FilterSector.TECHNOLOGY``."""
    cls_name, sep, member = spec.partition(".")
    if not sep or not member:
        raise ValueError(
            f"Filter spec must be 'ClassName.MEMBER', got {spec!r}. "
            f"Call list_filter_classes() to discover valid classes."
        )
    cls = _FILTER_CLASSES.get(cls_name)
    if cls is None:
        valid = ", ".join(sorted(_FILTER_CLASSES))
        raise ValueError(f"Unknown filter class {cls_name!r}. Valid classes: {valid}")
    try:
        return cls[member]
    except KeyError:
        valid = ", ".join(m.name for m in cls)
        raise ValueError(
            f"Unknown {cls_name} member {member!r}. Valid members: {valid}"
        ) from None


def resolve_filters(specs: Optional[Sequence[str]]) -> Optional[List[Enum]]:
    if not specs:
        return None
    return [resolve_filter(s) for s in specs]


def resolve_member(cls: Type[Enum], name: Optional[str]) -> Optional[Enum]:
    """Resolve a member of a specific enum class by name (no class prefix)."""
    if name is None:
        return None
    try:
        return cls[name]
    except KeyError:
        valid = ", ".join(m.name for m in cls)
        raise ValueError(
            f"Unknown {cls.__name__} member {name!r}. Valid members: {valid}"
        ) from None


def resolve_members(cls: Type[Enum], names: Optional[Sequence[str]]) -> Optional[List[Enum]]:
    if not names:
        return None
    return [resolve_member(cls, n) for n in names]  # type: ignore[list-item]


def resolve_ranges(
    raw: Optional[Dict[str, Sequence[Optional[float]]]],
) -> Optional[Dict[ScreenerRange, Tuple[Optional[float], Optional[float]]]]:
    """Convert ``{"PE": [10, 20]}`` to ``{ScreenerRange.PE: (10.0, 20.0)}``."""
    if not raw:
        return None
    out: Dict[ScreenerRange, Tuple[Optional[float], Optional[float]]] = {}
    for key, bounds in raw.items():
        try:
            metric = ScreenerRange[key]
        except KeyError:
            valid = ", ".join(m.name for m in ScreenerRange)
            raise ValueError(
                f"Unknown ScreenerRange member {key!r}. Valid: {valid}"
            ) from None
        if len(bounds) != 2:
            raise ValueError(
                f"Range for {key!r} must be a 2-element [min, max] list, got {bounds!r}"
            )
        lo, hi = bounds
        out[metric] = (
            None if lo is None else float(lo),
            None if hi is None else float(hi),
        )
    return out


def list_filter_classes() -> Dict[str, List[str]]:
    """Return ``{ClassName: [MEMBER, ...]}`` for all FilterXxx enum classes."""
    return {name: [m.name for m in cls] for name, cls in _FILTER_CLASSES.items()}


def list_enum(cls: Type[Enum]) -> List[str]:
    return [m.name for m in cls]
