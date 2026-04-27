import requests
from datetime import datetime
import json, os
import time
from config import API_KEY, BASE_URL, ZONE, BRONZE_PATH


def fetch(endpoint):
    url = f"{BASE_URL}/{endpoint}?zone={ZONE}"
    headers = {"auth-token": API_KEY}

    for i in range(3):  # retry 3 times
        try:
            r = requests.get(url, headers=headers)
            r.raise_for_status()
            return r.json(), url
        except Exception as e:
            print(f"Attempt {i+1} failed: {e}")
            time.sleep(2 ** i)  # exponential backoff

    raise Exception("API failed after retries")


def save(data, url):
    now = datetime.utcnow()
    path = f"{BRONZE_PATH}/year={now.year}/month={now.month}/day={now.day}"
    os.makedirs(path, exist_ok=True)

    record = {
        "data": data,
        "ingestion_timestamp": now.isoformat(),
        "source": url
    }

    with open(f"{path}/data_{now.hour}.json", "w") as f:
        json.dump(record, f)


def run():
    endpoints = ["power-breakdown/latest"]

    for ep in endpoints:
        try:
            data, url = fetch(ep)
            save(data, url)
        except Exception as e:
            print(f"Skipping {ep}: {e}")


if __name__ == "__main__":
    run()