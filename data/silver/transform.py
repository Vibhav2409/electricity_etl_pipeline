import pandas as pd
import glob
import json
import os
from config import BRONZE_PATH, SILVER_PATH

def read_bronze():
    files = glob.glob(f"{BRONZE_PATH}/**/*.json", recursive=True)
    records = []

    for file in files:
        with open(file) as f:
            records.append(json.load(f)["data"])

    return pd.json_normalize(records)

def transform(df):
    # Convert datetime
    df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")

    # Drop nulls
    df = df.dropna(subset=["datetime"])

    # Deduplicate
    df = df.drop_duplicates(subset=["zone", "datetime"])

    return df

def save_silver(df):
    df["year"] = df["datetime"].dt.year
    df["month"] = df["datetime"].dt.month
    df["day"] = df["datetime"].dt.day

    path = f"{SILVER_PATH}/"
    os.makedirs(path, exist_ok=True)

    df.to_parquet(path, partition_cols=["year", "month", "day"], index=False)

def run():
    df = read_bronze()
    df_clean = transform(df)
    save_silver(df_clean)

if __name__ == "__main__":
    run()