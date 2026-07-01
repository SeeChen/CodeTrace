"""Unit tests for the module-level run session."""

from codetrace import session
from codetrace.adapters.persistence import JsonPersistenceAdapter
from codetrace.config import Config
from codetrace.util.logging_setup import get_logger


def _make(tmp_path, **cfg_overrides):
    cfg = Config().merge(trace_root=str(tmp_path), **cfg_overrides)
    return session.get_or_create_session(cfg, JsonPersistenceAdapter(str(tmp_path)), get_logger())


def test_current_session_none_after_reset():
    session.reset_session()
    assert session.current_session() is None


def test_get_or_create_is_idempotent(tmp_path):
    first = _make(tmp_path)
    second = session.get_or_create_session(first.config, first.adapter, first.logger)
    assert first is second


def test_resolve_and_register(tmp_path):
    sess = _make(tmp_path)
    name1 = sess.resolve_trace_name("f")
    name2 = sess.resolve_trace_name("f")
    assert name1 == "f"
    assert name2 == "f__2"
    sess.register({"name": "f"})
    assert len(sess.records) == 1


def test_flush_summary_writes_once(tmp_path):
    sess = _make(tmp_path)
    sess.register({"name": "f", "duration": 0.1})
    sess.flush_summary()
    summary_path = tmp_path / sess.run_id / "summary.json"
    assert summary_path.exists()
    # Second flush is a no-op (does not raise, does not duplicate).
    sess.flush_summary()


def test_flush_summary_disabled_writes_nothing(tmp_path):
    sess = _make(tmp_path, summary=False)
    sess.register({"name": "f"})
    sess.flush_summary()
    assert not (tmp_path / sess.run_id / "summary.json").exists()


def test_module_flush_helper_is_safe_when_no_session():
    session.reset_session()
    # Should not raise even with no active session.
    session.flush()


def test_module_flush_writes_summary_when_session_exists(tmp_path):
    sess = _make(tmp_path)
    sess.register({"name": "f", "duration": 0.1})
    session.flush()
    assert (tmp_path / sess.run_id / "summary.json").exists()


def test_atexit_flush_writes_summary_when_session_exists(tmp_path):
    sess = _make(tmp_path)
    sess.register({"name": "f", "duration": 0.1})
    session._atexit_flush()
    assert (tmp_path / sess.run_id / "summary.json").exists()


def test_flush_summary_isolates_adapter_failure(tmp_path):
    """A failing summary write is logged and swallowed, never raised at exit."""

    class _BoomAdapter:
        def save_summary(self, *args, **kwargs):
            raise RuntimeError("summary boom")

    class _RecordingLogger:
        def __init__(self):
            self.warnings = []

        def warning(self, *args, **kwargs):
            self.warnings.append((args, kwargs))

    logger = _RecordingLogger()
    sess = session.Session(Config().merge(trace_root=str(tmp_path)), _BoomAdapter(), logger)
    sess.register({"name": "f"})
    sess.flush_summary()  # must not raise
    assert logger.warnings  # failure was recorded, not silently swallowed
