import json
from scraper.review import scrape_reviews

from models.reviews import Reviews

if __name__ == "__main__":
    with open("data/mapping.json", "r") as f:
        mapping = json.load(f)
        all_reviews = []
        for restaurant_id, restaurant_name in mapping.items():
            reviews = scrape_reviews(restaurant_id)

            for review in reviews:
                if review.comment == "":
                    continue

                review.restaurant_name = restaurant_name
                review.rating_food = review.rating.food
                review.rating_delivery = review.rating.delivery
                del review.rating

                all_reviews.append(review)

        res = Reviews(reviews=all_reviews)

        with open("data/reviews.json", "w") as f:
            f.write(res.json())
