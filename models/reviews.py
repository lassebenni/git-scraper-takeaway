from __future__ import annotations
from datetime import datetime

from typing import List, Optional

from pydantic import BaseModel, Field


class Rating(BaseModel):
    delivery: int
    food: int


class Review(BaseModel):
    rating: Optional[Rating]
    name: Optional[str]
    comment: Optional[str]
    date: Optional[datetime]
    time: Optional[str]
    is_sunday: Optional[bool] = Field(alias='isSunday')
    is_pickup: Optional[bool] = Field( alias='isPickup')
    is_new_year: Optional[bool] = Field( alias='isNewYear')
    restaurant_name: Optional[str]

class Reviews(BaseModel):
    reviews : List[Review]
