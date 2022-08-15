from collections import namedtuple
import json
import os
from typing import List, Tuple
from scraper.review import scrape_reviews
import concurrent.futures
import ray

from models.reviews import Reviews
from utils.aws import store_as_parquet

AWS_BUCKET_NAME = os.environ.get('AWS_BUCKET_NAME', "lbenninga-takeaway")

RestaurantMapping = namedtuple("Mapping", ["id", "name"])

@ray.remote
def scrape_and_store_reviews(mapping: RestaurantMapping):
    print(f"Scraping {mapping.name}")
    reviews = scrape_reviews(mapping.id)

    all_reviews = []
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
    print(f"Stored {mapping.name}")



def get_restaurant_id_mappings() -> List[RestaurantMapping]:
    with open("data/mapping.json", "r") as f:
        json_map = json.load(f)
        
        mappings = [RestaurantMapping(*m) for m in json_map.items()][:1]
        return mappings

if __name__ == "__main__":
    ray.init()
    mappings = get_restaurant_id_mappings()

    for map in mappings:
        scrape_and_store_reviews.remote(map)

    # refs = [scrape_and_store_reviews.remote(map) for map in mappings]
    # ray.get(refs)
