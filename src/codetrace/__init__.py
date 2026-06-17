"""CodeTrace: a lightweight, local-first, zero-dependency function tracer.

Primary entry point is :class:`TraceFunc`. The default hooks are exported for
users who want to wrap or extend them.
"""

from .compare import default_compare
from .recorder import default_record_builder
from .tracer import TraceFunc

__all__ = ["TraceFunc", "default_compare", "default_record_builder"]
__version__ = "0.1.0"
