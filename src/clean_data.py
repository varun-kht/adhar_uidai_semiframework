import pandas as pd

def validate_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Final sanity checks before modeling.
    Ensures required analytical columns exist and data is time-ordered.
    """
    required_cols = [
        "state",
        "month",
        "enrolment_count",
        "biometric_volume"
    ]

    missing = set(required_cols) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = df.sort_values(["state", "month"]).reset_index(drop=True)
    return df
