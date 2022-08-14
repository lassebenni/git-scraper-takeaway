from collections import namedtuple
import json
import os
from typing import Tuple
from scraper.review import scrape_reviews
import concurrent.futures

from models.reviews import Reviews
from utils.aws import store_as_parquet

AWS_BUCKET_NAME = os.environ.get('AWS_BUCKET_NAME', "lbenninga-takeaway")

RestaurantMapping = namedtuple("Mapping", ["id", "name"])

handled = 0

def scrape_and_store_reviews(mapping: RestaurantMapping):
    reviews = scrape_reviews(mapping.id)

    for review in reviews:
        if review.comment == "":
            continue

        review.restaurant_name = mapping.name
        review.rating_food = review.rating.food
        review.rating_delivery = review.rating.delivery
        del review.rating

        all_reviews.append(review)

    res = Reviews(reviews=all_reviews)
    res.store_as_parquet(bucket=AWS_BUCKET_NAME, path=f"data/{mapping.name}")

    handled += 1
    print(f"handled {handled}")



if __name__ == "__main__":
    with open("data/mapping.json", "r") as f:
        mapping = json.load(f)
        all_reviews = []
        
        print(f"total length: {len(mapping.items())}")
        mappings = [RestaurantMapping(*m) for m in mapping.items()]
        # scrape_and_store_reviews(mappings[0])
        # Scrape listings in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            executor.map(scrape_and_store_reviews, [RestaurantMapping(*x) for x in mapping.items()])