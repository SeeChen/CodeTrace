"""Unit tests for the Contract layer."""

from codetrace.adapters.persistence import JsonPersistenceAdapter
from codetrace.contracts import PersistenceAdapter


def test_json_adapter_satisfies_persistence_protocol():
    assert isinstance(JsonPersistenceAdapter(), PersistenceAdapter)


def test_partial_object_does_not_satisfy_protocol():
    class NotAnAdapter:
        def save_input(self, *args):
            pass

    assert not isinstance(NotAnAdapter(), PersistenceAdapter)
