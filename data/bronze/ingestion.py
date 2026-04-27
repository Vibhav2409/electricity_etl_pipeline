import requests
from datetime import datetime
import json, os
from config import API_KEY, BASE_URL, ZONE, BRONZE_PATH

def fetch(endpoint):
    url = f"{BASE_URL}/{endpoint}?zone={ZONE}"
    headers = {"auth-token": API_KEY}
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.json(), url

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
        data, url = fetch(ep)
        save(data, url)

if __name__ == "__main__":
    run()