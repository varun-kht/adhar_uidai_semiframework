import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler


def compute_priority_score(df: pd.DataFrame) -> pd.DataFrame:
    """
    Combines anomaly score, trend deviation score, and biometric load
    into a composite priority score and ranking.
    """

    df = df.copy()

    # Normalization
    scaler = MinMaxScaler()

    df[["anomaly_score", "trend_score", "biometric_volume"]] = scaler.fit_transform(
        df[["anomaly_score", "trend_score", "biometric_volume"]]
    )

    # priority score
    df["priority_score"] = (
        0.4 * df["anomaly_score"]
        + 0.3 * df["trend_score"]
        + 0.3 * df["biometric_volume"]
    )

  #ranking
    df = df.sort_values("priority_score", ascending=False)
    df["rank"] = range(1, len(df) + 1)

    return df


def add_explanations(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds human-readable explanations for why a state is flagged.
    """

    def explain(row):
        reasons = []

        if row["anomaly_score"] >= 0.7:
            reasons.append("Statistical anomaly in operational behaviour")

        if row["trend_score"] >= 0.6:
            reasons.append("Sharp deviation from historical enrolment trend")

        if row["biometric_volume"] >= 0.6:
            reasons.append("Sustained high biometric operational load")

        return "; ".join(reasons) if reasons else "No significant risk indicators"

    df = df.copy()
    df["why_flagged"] = df.apply(explain, axis=1)

    # FINAL OUTPUT COLUMNS 
    return df[
        [
            "state",
            "priority_score",
            "rank",
            "anomaly_score",
            "trend_score",
            "biometric_volume",
            "why_flagged",
        ]
    ]
