"""Unit tests for the safe serialization helper."""

from codetrace.util.serialization import safe_to_jsonable


def test_primitives_pass_through():
    assert safe_to_jsonable(1) == 1
    assert safe_to_jsonable("x") == "x"
    assert safe_to_jsonable(True) is True
    assert safe_to_jsonable(None) is None


def test_nested_containers_converted():
    value = {"a": [1, 2, {"b": (3, 4)}]}
    assert safe_to_jsonable(value) == {"a": [1, 2, {"b": [3, 4]}]}


def test_non_serializable_falls_back_to_repr():
    class Widget:
        def __repr__(self):
            return "<Widget>"

    assert safe_to_jsonable(Widget()) == "<Widget>"


def test_non_string_keys_are_stringified_safely():
    class Key:
        def __repr__(self):
            return "K"

    result = safe_to_jsonable({Key(): 1})
    assert result == {"K": 1}


def test_never_raises_on_hostile_repr():
    class Hostile:
        def __repr__(self):
            raise RuntimeError("boom")

    # Must not raise; returns a placeholder.
    assert safe_to_jsonable(Hostile()) == "<unserializable>"
