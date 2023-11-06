import os
from db.db import Page, engine
from db.sqlalchemy_client import SqlAlchemyClient
from scraper.scraper import Scraper
from indexer_client.indexer_client import IndexerClient
from crawler.web_crawler import WebCrawler

INDEXER_URL = os.environ.get("INDEXER_URL")

seed_pages = ["https://www.reddit.com/"]
db_client = SqlAlchemyClient(engine, Page)
indexer_client = IndexerClient(INDEXER_URL)

crawler = WebCrawler(seed_pages, Scraper, db_client, indexer_client, n_iters=1000)

if __name__ == "__main__":
    crawler.crawl()

