from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel, Field


class Indicators(BaseModel):
    is_delivery_by_scoober: bool = Field(..., alias="isDeliveryByScoober")
    is_new: bool = Field(..., alias="isNew")
    is_test_restaurant: bool = Field(..., alias="isTestRestaurant")
    is_grocery_store: bool = Field(..., alias="isGroceryStore")
    is_sponsored: bool = Field(..., alias="isSponsored")


class Brand(BaseModel):
    name: str
    logo_url: str = Field(..., alias="logoUrl")
    hero_image_url: str = Field(..., alias="heroImageUrl")
    hero_image_url_type: str = Field(..., alias="heroImageUrlType")
    branch_name: str = Field(..., alias="branchName")


class Rating(BaseModel):
    votes: int
    score: float


class Location(BaseModel):
    street_address: str = Field(..., alias="streetAddress")
    city: str
    country: str
    lat: str
    lng: str
    time_zone: str = Field(..., alias="timeZone")


class Supports(BaseModel):
    delivery: bool
    pickup: bool
    vouchers: bool
    stamp_cards: bool = Field(..., alias="stampCards")
    discounts: bool


class DurationRange(BaseModel):
    min: int
    max: int


class LowestDeliveryFee(BaseModel):
    from_: int = Field(..., alias="from")
    fee: int


class DynamicDeliveryFeeInfo(BaseModel):
    expiry_time: Optional[int] = Field(alias="expiryTime")
    token: Optional[str]


class Delivery(BaseModel):
    is_open_for_order: bool = Field(..., alias="isOpenForOrder")
    is_open_for_preorder: bool = Field(..., alias="isOpenForPreorder")
    opening_time: Any = Field(..., alias="openingTime")
    duration: int
    duration_range: DurationRange = Field(..., alias="durationRange")
    delivery_fee_default: int = Field(..., alias="deliveryFeeDefault")
    min_order_value: int = Field(..., alias="minOrderValue")
    lowest_delivery_fee: LowestDeliveryFee = Field(..., alias="lowestDeliveryFee")
    dynamic_delivery_fee_info: DynamicDeliveryFeeInfo = Field(
        ..., alias="dynamicDeliveryFeeInfo"
    )


class Distance(BaseModel):
    unit: str
    quantity: int


class Pickup(BaseModel):
    is_open_for_order: bool = Field(..., alias="isOpenForOrder")
    is_open_for_preorder: bool = Field(..., alias="isOpenForPreorder")
    opening_time: Any = Field(..., alias="openingTime")
    distance: Distance


class ShippingInfo(BaseModel):
    delivery: Delivery
    pickup: Pickup


class Restaurant(BaseModel):
    id: str
    primary_slug: str = Field(..., alias="primarySlug")
    indicators: Indicators
    price_range: int = Field(..., alias="priceRange")
    popularity: int
    brand: Brand
    cuisine_types: Optional[List[str]] = Field(alias="cuisineTypes")
    rating: Rating
    location: Location
    supports: Supports
    shipping_info: ShippingInfo = Field(..., alias="shippingInfo")
    payment_methods: List[str] = Field(..., alias="paymentMethods")
