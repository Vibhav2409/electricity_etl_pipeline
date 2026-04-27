# Electricity Maps ETL Pipeline

## Overview
Medallion Architecture pipeline (Bronze → Silver → Gold)
for France electricity data.

## Tech Stack
- PySpark
- Delta Lake
- Airflow

## Setup

pip install -r requirements.txt

export API_KEY=your_key

## Run

python src/ingestion.py
python src/silver.py
python src/gold.py

## Output

- Bronze → raw JSON
- Silver → Delta tables
- Gold → analytics tables

## Bonus Features
- Delta Lake (ACID)
- Deduplication with window
- Airflow orchestration
