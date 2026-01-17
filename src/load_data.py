import pandas as pd

def load_processed_data(path: str) -> pd.DataFrame:
    """
    Loads the cleaned & feature-engineered dataset.
    """
    df = pd.read_csv(path)
    df["month"] = pd.to_datetime(df["month"])
    return df
