from scraper.restaurant import scrape_restaurants
from scraper.review import scrape_reviews

from models.reviews import Reviews

if __name__ == '__main__':
    restaurants = scrape_restaurants()
    all_reviews = []
    for restaurant in restaurants:
        reviews = scrape_reviews(restaurant.id)

        for review in reviews.reviews:
            if review.comment == "":
                continue

            review.restaurant_name = restaurant.primary_slug
            review.rating_food = review.rating.food
            review.rating_delivery = review.rating.delivery
            del review.rating

            all_reviews.append(review)
            break
        break

    res = Reviews(reviews=all_reviews)

    with open('data/reviews.json', 'w') as f:
        f.write(res.json())