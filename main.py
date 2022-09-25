from dask.distributed import Client
from scraper.reviews_scraper import ReviewsScraper


if __name__ == "__main__":
    client = Client()
    scraper = ReviewsScraper()
    scraper.scrape(client)
