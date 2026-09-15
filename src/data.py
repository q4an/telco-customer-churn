import pandas as pd 
from pathlib import Path
from sklearn.model_selection import train_test_split

DATA_PATH = (
    Path(__file__).resolve().parent.parent
    /"data"
    /"Telco-Customer-Churn.csv"
)


def load_data(path=DATA_PATH):
    df = pd.read_csv(path)
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    return df


def split_data(df, test_size=0.2, random_state=42):
    train_set, test_set = train_test_split(
        df,
        test_size=test_size,
        random_state=random_state,
        stratify=df["Churn"]
    )

    return train_set, test_set
