from __future__ import annotations
from datetime import datetime

from typing import Optional

from pydantic import BaseModel, Field
from uuid import UUID, uuid4



class Rating(BaseModel):
    delivery: int
    food: int


class Review(BaseModel):
    updated: datetime = Field(default_factory=datetime.now)
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
