"""turbokain — Python orchestration layer for the TurboKain Kain exes.

This package does NOT detect anything. The detectors are native Kain exes in
``kain/``. Python's job here is glue: discover the exes, invoke them with a
stable contract, run their built-in self-tests, chain them into a unified scan,
and harvest receipts (stdout + tables + sidecar manifest).

See ``python/README.md`` and the "Python is allowed" section of ``AGENTS.md``.
"""

from .registry import Tool, Registry, load_registry
from .runner import RunResult, run_tool, run_selftest, repo_root
from .scan import ScanPlan, run_scan

__all__ = [
    "Tool",
    "Registry",
    "load_registry",
    "RunResult",
    "run_tool",
    "run_selftest",
    "repo_root",
    "ScanPlan",
    "run_scan",
]

__version__ = "0.1.0"
