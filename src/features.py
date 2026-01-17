import pandas as pd

def generate_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates final operational signals used for ML & scoring.
    Assumes input is a state-month level dataset.
    """
    df = df.copy()

    # Enrolment month-over-month change
    df["enrolment_change"] = (
        df.groupby("state")["enrolment_count"]
        .pct_change()
    )

    # Rolling enrolment baseline
    df["enrolment_rolling_mean"] = (
        df.groupby("state")["enrolment_count"]
        .rolling(3, min_periods=1)
        .mean()
        .reset_index(level=0, drop=True)
    )

    # Rolling biometric baseline
    df["biometric_rolling_mean"] = (
        df.groupby("state")["biometric_volume"]
        .rolling(3, min_periods=1)
        .mean()
        .reset_index(level=0, drop=True)
    )

    return df
