"""Reusable data loading utilities for manufacturing datasets."""

from pathlib import Path
from typing import Any

import pandas as pd


def load_csv(path: str | Path, **read_kwargs: Any) -> pd.DataFrame:
    """
    Load a CSV file into a pandas DataFrame.

    Args:
        path: File path to the dataset.
        **read_kwargs: Extra arguments forwarded to pandas.read_csv.

    Returns:
        Loaded DataFrame.
    """
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Dataset not found: {file_path}")
    return pd.read_csv(file_path, **read_kwargs)


def load_timeseries(
    path: str | Path,
    timestamp_col: str = "timestamp",
    **read_kwargs: Any,
) -> pd.DataFrame:
    """
    Load time-series manufacturing data and parse timestamps.

    Placeholder: extend with resampling, timezone handling, and validation.
    """
    df = load_csv(path, **read_kwargs)
    if timestamp_col in df.columns:
        df[timestamp_col] = pd.to_datetime(df[timestamp_col])
        df = df.sort_values(timestamp_col)
    return df


def sample_rows(df: pd.DataFrame, n: int = 100) -> pd.DataFrame:
    """Return a small sample for prototyping and notebook workflows."""
    return df.head(n) if len(df) <= n else df.sample(n=n, random_state=42)
