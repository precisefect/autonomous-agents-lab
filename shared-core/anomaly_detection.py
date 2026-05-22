"""Placeholder anomaly detection helpers for industrial sensor data."""

from typing import Any

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest


def detect_anomalies_zscore(
    series: pd.Series,
    threshold: float = 3.0,
) -> pd.Series:
    """
    Flag anomalies using z-score on a numeric series.

    Returns:
        Boolean mask where True indicates a likely anomaly.
    """
    mean = series.mean()
    std = series.std()
    if std == 0 or np.isnan(std):
        return pd.Series(False, index=series.index)
    z = (series - mean) / std
    return z.abs() > threshold


def detect_anomalies_isolation_forest(
    df: pd.DataFrame,
    columns: list[str] | None = None,
    contamination: float = 0.05,
    random_state: int = 42,
) -> pd.Series:
    """
    Unsupervised anomaly detection via Isolation Forest.

    Placeholder: swap model, features, and contamination per line/equipment.
    """
    feature_cols = columns or df.select_dtypes(include=[np.number]).columns.tolist()
    if not feature_cols:
        raise ValueError("No numeric columns available for anomaly detection")

    X = df[feature_cols].fillna(df[feature_cols].median())
    model = IsolationForest(
        contamination=contamination,
        random_state=random_state,
    )
    labels = model.fit_predict(X)
    # IsolationForest: -1 = anomaly, 1 = normal
    return pd.Series(labels == -1, index=df.index, name="is_anomaly")


def summarize_anomalies(mask: pd.Series) -> dict[str, Any]:
    """Aggregate anomaly counts for dashboards and alerting."""
    total = len(mask)
    count = int(mask.sum())
    return {
        "total_points": total,
        "anomaly_count": count,
        "anomaly_rate": round(count / total, 4) if total else 0.0,
    }
