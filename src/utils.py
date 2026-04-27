import time
import requests

def retry_api_call(url, headers, retries=3):
    for i in range(retries):
        try:
            r = requests.get(url, headers=headers)
            r.raise_for_status()
            return r.json()
        except Exception:
            time.sleep(2 ** i)
    raise Exception("API failed after retries")