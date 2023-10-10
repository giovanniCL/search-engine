import os
from db import Page, engine
from scraper import Scraper
from sqlalchemy_client import SqlAlchemyClient
from indexer_client import IndexerClient
from web_crawler import WebCrawler

INDEXER_URL = os.environ.get("INDEXER_URL")

seed_pages = ["https://www.reddit.com/"]
db_client = SqlAlchemyClient(engine, Page)
indexer_client = IndexerClient(INDEXER_URL)

crawler = WebCrawler(seed_pages, Scraper, db_client, indexer_client, n_iters=1000)
crawler.crawl()

