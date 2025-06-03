import time

import requests
from os import getenv
from dotenv import load_dotenv

load_dotenv()
API_KEY = getenv("API_KEY_EXCHANGERATE")

cache = {}
CACHE_TTL = 3600


def get_currency(base_currency: str = "USD", to_currency: str = None):
    current_time = time.time()
    if base_currency in cache:
        cached_data, timestamp = cache[base_currency]
        if current_time - timestamp < CACHE_TTL:
            if to_currency:
                print("Использовалось Из кеша")
                return cached_data["conversion_rates"].get(to_currency)
            return cached_data["conversion_rates"]
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{base_currency}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        cache[base_currency] = data, current_time
        if to_currency:
            print("Использовалось Из апи")
            return data["conversion_rates"].get(to_currency)
        return data["conversion_rates"]
    else:
        print(f"Ошибка API: {response.status_code}")
    return None
