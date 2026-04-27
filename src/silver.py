import pandas as pd
import glob
import json
import os
from datetime import datetime
from config import BRONZE_PATH, SILVER_PATH

# 🔹 Read all bronze files
files = glob.glob(f"{BRONZE_PATH}/**/*.json", recursive=True)

records = []
for file in files:
    with open(file) as f:
        data = json.load(f)
        record = data["data"]
        record["ingestion_timestamp"] = data["ingestion_timestamp"]
        records.append(record)

# 🔹 Convert to DataFrame
df = pd.json_normalize(records)

# 🔹 Convert datetime
df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")

# 🔹 Drop nulls
df = df.dropna(subset=["datetime"])

# 🔹 Deduplicate (same logic as Spark)
df = df.sort_values("ingestion_timestamp", ascending=False)
df = df.drop_duplicates(subset=["zone", "datetime"])

# 🔹 Add partition columns
df["year"] = df["datetime"].dt.year
df["month"] = df["datetime"].dt.month
df["day"] = df["datetime"].dt.day

# 🔹 Save as Parquet (Silver)
output_path = f"{SILVER_PATH}"
os.makedirs(output_path, exist_ok=True)

df.to_parquet(
    output_path,
    partition_cols=["year", "month", "day"],
    index=False
)

print("✅ Silver layer created successfully")