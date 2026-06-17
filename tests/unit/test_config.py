"""Unit tests for configuration merge and validation."""

import pytest

from codetrace.config import Config


def test_defaults():
    cfg = Config()
    assert cfg.enabled is True
    assert cfg.persistence is True
    assert cfg.trace_root == ".codetrace"
    assert cfg.metrics_collectors == ()


def test_merge_is_scoped_and_non_mutating():
    base = Config()
    scoped = base.merge(persistence=False)
    assert scoped.persistence is False
    assert base.persistence is True  # original untouched


def test_unknown_key_raises():
    with pytest.raises(ValueError):
        Config().merge(nonsense=True)


def test_reserved_metrics_collectors_accepted():
    cfg = Config().merge(metrics_collectors=("x",))
    assert cfg.metrics_collectors == ("x",)
