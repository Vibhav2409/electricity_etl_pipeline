import pandas as pd
import glob
import os
from config import SILVER_PATH, GOLD_PATH

def read_silver():
    files = glob.glob(f"{SILVER_PATH}/**/*.parquet", recursive=True)
    df = pd.concat([pd.read_parquet(f) for f in files])
    return df

def daily_mix(df):
    df["date"] = df["datetime"].dt.date

    energy_cols = [col for col in df.columns if "production" in col]

    daily = df.groupby("date")[energy_cols].sum()

    total = daily.sum(axis=1)

    for col in energy_cols:
        daily[col + "_pct"] = (daily[col] / total) * 100

    return daily.reset_index()

def save_gold(df, name):
    path = f"{GOLD_PATH}/{name}.parquet"
    os.makedirs(GOLD_PATH, exist_ok=True)
    df.to_parquet(path, index=False)

def run():
    df = read_silver()
    mix = daily_mix(df)
    save_gold(mix, "daily_mix")

if __name__ == "__main__":
    run()