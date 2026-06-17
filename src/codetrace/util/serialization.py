"""Safe JSON serialization helpers.

Converts arbitrary Python values into JSON-native structures, falling back to
``repr(value)`` for anything that is not natively serializable. These helpers
must never raise into user code.
"""

from typing import Any

_PRIMITIVES = (str, int, float, bool)


def safe_to_jsonable(value: Any) -> Any:
    """Convert ``value`` into a JSON-serializable structure.

    Primitives and nested ``dict``/``list``/``tuple``/``set`` structures are
    converted recursively. Any other value falls back to ``repr(value)``. This
    function never raises; on an unexpected error it returns a placeholder
    string.

    Args:
        value: Any Python value.

    Returns:
        A JSON-serializable representation of ``value``.
    """
    try:
        return _convert(value)
    except Exception:  # noqa: BLE001 - serialization must never raise into user code
        try:
            return repr(value)
        except Exception:  # noqa: BLE001
            return "<unserializable>"


def _convert(value: Any) -> Any:
    """Recursively convert a value to a JSON-native structure."""
    if value is None or isinstance(value, _PRIMITIVES):
        return value
    if isinstance(value, dict):
        return {_safe_key(key): _convert(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set, frozenset)):
        return [_convert(item) for item in value]
    return repr(value)


def _safe_key(key: Any) -> Any:
    """Return a JSON-compatible mapping key."""
    if key is None or isinstance(key, _PRIMITIVES):
        return key
    return repr(key)
