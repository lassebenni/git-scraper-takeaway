from __future__ import annotations
from datetime import datetime

from typing import List, Optional, Union

from pydantic import BaseModel, Field
from uuid import UUID, uuid4
import pandas as pd

from utils.aws import store_as_parquet


class Rating(BaseModel):
    delivery: int
    food: int


class Review(BaseModel):
    uid: UUID = Field(default_factory=uuid4)
    rating: Optional[Rating]
    rating_delivery: Optional[int]
    rating_food: Optional[int]
    name: Optional[str]
    comment: Optional[str]
    date: Optional[datetime]
    time: Optional[str]
    is_sunday: Optional[bool] = Field(alias="isSunday")
    is_pickup: Optional[bool] = Field(alias="isPickup")
    is_new_year: Optional[bool] = Field(alias="isNewYear")
    restaurant_name: Optional[str]


class Reviews(BaseModel):
    reviews: List[Review]
    ingestion_date: datetime = datetime.today().strftime("%d-%m-%y")

    def _to_dataframe(self) ->pd.DataFrame:
        df = pd.DataFrame.from_dict([x.dict() for x in self.reviews])
        df['ingestion_date'] = self.ingestion_date
        df['uid'] = df['uid'].astype(str)
        return df


    def store_as_parquet(self, bucket: str, path: str):
        df = self._to_dataframe()
        store_as_parquet(df=df, bucket=bucket, path=path)
