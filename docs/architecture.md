# Architecture

## Application View
- Bronze: raw ingestion
- Silver: cleaned structured data
- Gold: aggregated analytics

## Infrastructure
- Spark + Delta Lake
- Local / S3 storage
- Airflow orchestration

## RAG Design
- Gold layer used for structured retrieval
- Vector DB for unstructured docs
- LLM generates grounded responses