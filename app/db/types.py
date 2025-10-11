from __future__ import annotations

import json
from typing import Any

from sqlalchemy.types import TEXT, TypeDecorator

try:
    from sqlalchemy.dialects.mysql import JSON as MySQLJSON  # type: ignore

    JSONType = MySQLJSON  # Native MySQL JSON support
    HAS_NATIVE_JSON = True
except ImportError:  # pragma: no cover - fallback for non-MySQL environments
    JSONType = None  # Sentinel until JSONString is defined
    HAS_NATIVE_JSON = False


class JSONString(TypeDecorator):  # pragma: no cover - simple serialization helper
    """
    Lightweight JSON serializer for databases lacking native JSON columns.
    Stores Python dict/list structures as JSON strings while keeping the ORM
    interface identical to native JSON columns.
    """

    impl = TEXT
    cache_ok = True

    def process_bind_param(self, value: Any, dialect: Any) -> Any:
        if value is None:
            return None
        return json.dumps(value, ensure_ascii=False)

    def process_result_value(self, value: Any, dialect: Any) -> Any:
        if value is None:
            return None
        try:
            return json.loads(value)
        except (TypeError, ValueError):
            return value


if JSONType is None:  # pragma: no cover - executed only when MySQL JSON is unavailable
    JSONType = JSONString

__all__ = ["JSONType", "HAS_NATIVE_JSON", "JSONString"]
