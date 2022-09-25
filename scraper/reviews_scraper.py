from collections import namedtuple
import json
import os
from typing import Dict, List
from models.reviews import Review
from models.reviews_parser import ReviewsParser
from scraper.rest.review import scrape_reviews
from dask.distributed import Client

from utils.general import flatten


AWS_BUCKET_NAME = os.environ.get('AWS_BUCKET_NAME', "lbenninga-takeaway")

RestaurantMapping = namedtuple("Mapping", ["id", "name"])

class ReviewsScraper:

    def __init__(self):
        self.parser = ReviewsParser()
        self.mappings = self._get_restaurant_id_mappings()


    def scrape(self,client: Client):
        futures = client.map(self._scrape_in_parralel, self.mappings)
        for future in futures:
            future.result()

        reviews: List[Review] = flatten(client.gather(futures))
        self.parser.store_reviews(reviews)

    def _scrape_in_parralel(self, mapping: RestaurantMapping) -> List[Review]:
        print(f"Scraping {mapping.name}")
        reviews_json: List[Dict] = scrape_reviews(mapping.id)

        reviews: List[Review] = self.parser.parse_reviews(mapping.name, reviews_json)
        print(f"Scraped {len(reviews)} reviews for {mapping.name}")

        return reviews

    def _get_restaurant_id_mappings(self) -> List[RestaurantMapping]:
        with open("data/mapping.json", "r") as f:
            json_map = json.load(f)
            mappings = [RestaurantMapping(*m) for m in json_map.items()]
            return [mappings[0]]
