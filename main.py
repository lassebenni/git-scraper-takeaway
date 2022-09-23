from collections import namedtuple
from datetime import datetime
import json
import os
from typing import List, Tuple
from scraper.review import scrape_reviews
from dask.distributed import Client, Variable


from models.reviews import ReviewsParser
from utils.aws import store_as_parquet

AWS_BUCKET_NAME = os.environ.get('AWS_BUCKET_NAME', "lbenninga-takeaway")

RestaurantMapping = namedtuple("Mapping", ["id", "name"])


def scrape_and_store_reviews(parser: ReviewsParser, mapping: RestaurantMapping):
    print(f"Scraping {mapping.name}")
    reviews = scrape_reviews(mapping.id)
    print(f"Scraped reviews for {mapping.name}")



    for review in reviews:
        if review.comment == "":
            continue

        review.restaurant_name = mapping.name
        review.rating_food = review.rating.food
        review.rating_delivery = review.rating.delivery
        del review.rating

        parser.reviews.appendreviews)


    # if res.reviews:
    #     today = datetime.today().strftime("%d-%m-%y")
    #     res.store_as_parquet(bucket=AWS_BUCKET_NAME, path=f"data/{today}/{mapping.name}")
    
    handled = global_var.get()
    handled += 1
    print(handled)
    global_var.set(handled)


def get_restaurant_id_mappings() -> List[RestaurantMapping]:
    with open("data/mapping.json", "r") as f:
        json_map = json.load(f)
        
        mappings = [RestaurantMapping(*m) for m in json_map.items()]
        return mappings

if __name__ == "__main__":
    client = Client()
    global_var = Variable(name="handled")
    global_var.set(0)

    mappings = get_restaurant_id_mappings()

    reviews_scraper = 
    futures = client.map(scrape_and_store_reviews, mappings)
    for future in futures:
        future.result()

    print("Finished.")
