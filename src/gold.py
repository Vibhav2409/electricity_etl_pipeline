import pandas as pd
import glob
import os
from config import SILVER_PATH, GOLD_PATH

# 🔹 Read all Silver parquet files
files = glob.glob(f"{SILVER_PATH}/**/*.parquet", recursive=True)

df = pd.concat([pd.read_parquet(f) for f in files])

# 🔹 Convert datetime → date
df["date"] = pd.to_datetime(df["datetime"]).dt.date

# 🔹 Identify energy columns
energy_cols = [c for c in df.columns if "production" in c]

# 🔹 Aggregate daily sums
agg = df.groupby("date")[energy_cols].sum().reset_index()

# 🔹 Calculate total per row
agg["total"] = agg[energy_cols].sum(axis=1)

# 🔹 Calculate percentage contribution
for c in energy_cols:
    agg[f"{c}_pct"] = (agg[c] / agg["total"]) * 100

# 🔹 Drop total column (optional)
agg = agg.drop(columns=["total"])

# 🔹 Save Gold output
os.makedirs(GOLD_PATH, exist_ok=True)

agg.to_parquet(f"{GOLD_PATH}/daily_mix.parquet", index=False)

print("✅ Gold layer (daily mix) created successfully")