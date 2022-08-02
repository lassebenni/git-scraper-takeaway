import requests
import json

from models.reviews import Reviews


payload={}
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:102.0) Gecko/20100101 Firefox/102.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.thuisbezorgd.nl/',
    'X-Language-Code': 'en',
    'X-Country-Code': 'nl',
    'X-Session-ID': '85c14822-75ed-4f70-bd0e-403e42dc7173',
    'X-Requested-With': 'XMLHttpRequest',
    'x-datadog-origin': 'rum',
    'x-datadog-parent-id': '892796564123353268',
    'x-datadog-sampled': '1',
    'x-datadog-sampling-priority': '1',
    'x-datadog-trace-id': '2052618133631691932',
    'Origin': 'https://www.thuisbezorgd.nl',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'TE': 'trailers',
}

def scrape_reviews(restaurant_id: str) -> list[Reviews]:
    url = f"https://cw-api.takeaway.com/api/v31/restaurant/reviews?id={restaurant_id}&page=0"
    response = requests.request("GET", url, headers=headers, data=payload)
    reviews_json = json.loads(response.text)

    return Reviews(**reviews_json)
