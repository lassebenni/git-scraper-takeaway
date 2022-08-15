import time
import requests
import json
import itertools

from models.reviews import Reviews


payload = {}
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:102.0) Gecko/20100101 Firefox/102.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.thuisbezorgd.nl/",
    "X-Language-Code": "en",
    "X-Country-Code": "nl",
    "X-Session-ID": "85c14822-75ed-4f70-bd0e-403e42dc7173",
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
    "Cookie": "__cf_bm=uCRKXYHao_w8eM0sXunMW0Ix8TH7CosSzn.9jXjhQko-1659476159-0-AbQWQX/i1/iB4lplWr24sLb+DBNiZi7HgMN69JrMyBG6jow7wM3ORuQl2ZwQhchCiEc3aljbR+w7dFEwu7/ZgiCv8ioAtVJG+sX+u5k7dSce",
}


def scrape_reviews(restaurant_id: str, limit: int = 0) -> list[Reviews]:
    reviews = []

    page = 0
    scraped_all = False
    while not scraped_all:
        url = f"https://cw-api.takeaway.com/api/v31/restaurant/reviews?id={restaurant_id}&page={page}"
        response = requests.request("GET", url, headers=headers, data=payload)

        if response:
            reviews_json = json.loads(response.text)
            if reviews_json["reviews"]:
                reviews.append(Reviews(**reviews_json))

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
    reviews = flatten([x.reviews for x in reviews])

    return reviews


def flatten(list_of_lists):
    return list(itertools.chain.from_iterable(list_of_lists))
