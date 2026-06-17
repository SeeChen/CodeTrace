"""Shared pytest fixtures for the CodeTrace test suite."""

import pytest

from codetrace import session
from codetrace.config import Config
from codetrace.tracer import TraceFunc


@pytest.fixture(autouse=True)
def reset_state():
    """Reset the singleton session and global config around every test."""
    session.reset_session()
    TraceFunc._global_config = Config()
    yield
    session.reset_session()
    TraceFunc._global_config = Config()


@pytest.fixture
def trace_root(tmp_path):
    """Point the tracer at an isolated temp trace root and return its path."""
    root = tmp_path / ".codetrace"
    TraceFunc.config(trace_root=str(root))
    return root
