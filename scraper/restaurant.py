import requests
import json

from models.restaurant import Restaurant


url = "https://cw-api.takeaway.com/api/v31/restaurants?deliveryAreaId=936874&postalCode=3511&lat=52.08944030000001&lng=5.1099869&limit=0&isAccurate=false"

payload={}
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:102.0) Gecko/20100101 Firefox/102.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.thuisbezorgd.nl/',
    'X-Language-Code': 'en',
    'X-Country-Code': 'nl',
    'X-Session-ID': '8070b889-a1bc-4205-a2cc-4aed0a3c8e50',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://www.thuisbezorgd.nl',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'TE': 'trailers',
    'Cookie': '__cf_bm=VthKD.EertRh30SheMdiRtk8nOEya9_wMqymvmyT5Qg-1659468095-0-ASKMDZSW+hnKw1B4NRPjLVigazSp4UbzC1MXNINpjAY20A+jtRyPtdxu1/U7yp9nfbJ0SAklaEvyIcyZi8C0GKrr3q2STvdUPLsgPB8y+BRX'
}

def scrape_restaurants() -> list[Restaurant]:
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.status_code)
    restaurants_json = json.loads(response.text)['restaurants']

    return [Restaurant(**restaurants_json[val]) for k, val in enumerate(restaurants_json)]
