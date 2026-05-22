"""Resolve and expose the lab-wide shared-core package on sys.path."""

import sys
from pathlib import Path


def _agent_root() -> Path:
    """Directory containing main.py (two levels above app/utils)."""
    return Path(__file__).resolve().parents[2]


def _find_shared_core(start: Path) -> Path | None:
    """Walk up from start until a shared-core directory is found."""
    for parent in (start, *start.parents):
        candidate = parent / "shared-core"
        if candidate.is_dir() and (candidate / "data_loader.py").exists():
            return candidate
    return None


def ensure_shared_core_on_path() -> Path:
    """
    Add shared-core to sys.path so modules import as:
        import data_loader
        import anomaly_detection
        import alerting
    """
    root = _agent_root()
    shared = root / "shared-core"
    if not shared.is_dir():
        found = _find_shared_core(root)
        if found is None:
            raise RuntimeError(
                "shared-core not found. Run from the lab repo or copy "
                "shared-core into the agent directory."
            )
        shared = found

    path_str = str(shared.resolve())
    if path_str not in sys.path:
        sys.path.insert(0, path_str)
    return shared
