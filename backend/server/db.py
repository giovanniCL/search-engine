import os
from sqlalchemy import create_engine

CRAWLER_DB_HOST = os.environ.get("CRAWLER_DB_HOST")
CRAWLER_DB_PORT = os.environ.get("CRAWLER_DB_PORT")
CRAWLER_DB_NAME = os.environ.get("CRAWLER_DB_NAME")
CRAWLER_DB_USER = os.environ.get("CRAWLER_DB_USER")
CRAWLER_DB_PASSWORD = os.environ.get("CRAWLER_DB_PASSWORD")

INDEXER_DB_HOST = os.environ.get("INDEXER_DB_HOST")
INDEXER_DB_PORT = os.environ.get("INDEXER_DB_PORT")
INDEXER_DB_NAME = os.environ.get("INDEXER_DB_NAME")
INDEXER_DB_USER = os.environ.get("INDEXER_DB_USER")
INDEXER_DB_PASSWORD = os.environ.get("INDEXER_DB_PASSWORD")

crawler_db_connection_string = \
    f"postgresql+psycopg2://{CRAWLER_DB_USER}:{CRAWLER_DB_PASSWORD}@{CRAWLER_DB_HOST}:{CRAWLER_DB_PORT}/{CRAWLER_DB_NAME}"

indexer_db_connection_string = \
    f"postgresql+psycopg2://{INDEXER_DB_USER}:{INDEXER_DB_PASSWORD}@{INDEXER_DB_HOST}:{INDEXER_DB_PORT}/{INDEXER_DB_NAME}"


indexer_engine = create_engine(indexer_db_connection_string, echo=True)
crawler_engine = create_engine(crawler_db_connection_string, echo=True)