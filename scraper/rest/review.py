import time
from typing import Dict, List
import requests
import json
import itertools

from utils.general import flatten

payload = {}
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:102.0) Gecko/20100101 Firefox/102.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.thuisbezorgd.nl/",
    "X-Language-Code": "en",
    "X-Country-Code": "nl",
    "X-Requested-With": "XMLHttpRequest",
    "x-datadog-origin": "rum",
    "x-datadog-parent-id": "892796564123353268",
    "x-datadog-sampled": "1",
    "x-datadog-sampling-priority": "1",
    "x-datadog-trace-id": "2052618133631691932",
    "Origin": "https://www.thuisbezorgd.nl",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "TE": "trailers",
}


def scrape_reviews(restaurant_id: str, limit: int = 0) -> List[Dict]:
    reviews = []

    page = 0
    scraped_all = False
    while not scraped_all:
        url = f"https://cw-api.takeaway.com/api/v31/restaurant/reviews?id={restaurant_id}&page={page}"
        response = requests.request("GET", url, headers=headers, data=payload)

        print(response.status_code)
        if response:
            reviews_json = json.loads(response.text)
            if reviews_json["reviews"]:
                reviews.append(reviews_json)

                page += 1
                if limit > 0 and page >= limit:
                    break
                else:
                    time.sleep(1)
            else:
                scraped_all = True
        else:
            scraped_all = True

    # flatten into single list
    return flatten([x['reviews'] for x in reviews])
