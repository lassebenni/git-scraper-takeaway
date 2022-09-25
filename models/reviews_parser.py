from __future__ import annotations
from datetime import datetime
import json

from typing import Dict, List

import pandas as pd
from models.reviews import Review

from utils.aws import store_as_parquet

class ReviewsParser():
    # def _to_dataframe(self) ->pd.DataFrame:
    #     df = pd.DataFrame.from_dict([x.dict() for x in self.reviews])
    #     df['ingestion_date'] = self.ingestion_date
    #     df['uid'] = df['uid'].astype(str)
    #     return df


    def store_as_parquet(self, bucket: str, path: str):
        df = self._to_dataframe()
        store_as_parquet(df=df, bucket=bucket, path=path)

    def parse_reviews(self, restaurant_name, reviews_json: List[Dict]) -> List[Review]:
        reviews: List[Review] = []
        for review in reviews_json:
            if review['comment'] == "":
                continue

            review['restaurant_name'] = restaurant_name
            review['rating_food'] = review['rating']['food']
            review['rating_delivery'] = review['rating']['delivery']

            reviews.append(Review(**review))

        return reviews


    def store_reviews(self, reviews: List[Review]):
        with open('data/scraped_reviews.json', 'w') as f:
            json.dump([review.dict() for review in reviews], f, default=str)