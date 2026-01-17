import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import MinMaxScaler


def compute_trend_score(df: pd.DataFrame) -> pd.DataFrame:
    """
    Measures recent deviation from historical enrolment baseline.
    Higher score = stronger deviation from normal behaviour.
    """
    df = df.copy()

    df["trend_deviation"] = (
        df["enrolment_count"] - df["enrolment_rolling_mean"]
    ) / df["enrolment_rolling_mean"]

    trend_score = (
        df.groupby("state")["trend_deviation"]
        .last()
        .abs()
        .reset_index(name="trend_score")
    )

    return trend_score


def compute_anomaly_score(df: pd.DataFrame) -> pd.DataFrame:
    """
    Detects operational anomalies using enrolment volatility
    and biometric load signals.
    """
    features = (
        df.groupby("state")
        .agg({
            "enrolment_change": "mean",
            "biometric_volume": "mean"
        })
        .fillna(0)
    )

    model = IsolationForest(
        n_estimators=100,
        contamination=0.2,
        random_state=42
    )

    features["anomaly_raw"] = model.fit_predict(features)

    # Convert {-1, 1} → {1, 0} where higher = more anomalous
    features["anomaly_score"] = (features["anomaly_raw"] == -1).astype(int)

    return features[["anomaly_score"]].reset_index()


def normalize_scores(df: pd.DataFrame, cols: list) -> pd.DataFrame:
    """
    Min-max normalization for combining heterogeneous scores.
    """
    scaler = MinMaxScaler()
    df[cols] = scaler.fit_transform(df[cols])
    return df
