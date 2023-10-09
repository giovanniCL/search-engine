from sqlalchemy import String, Integer, create_engine
from sqlalchemy.orm import mapped_column, DeclarativeBase

indexer_engine = create_engine('postgresql+psycopg2://debug:debug\
@indexerdb:5433/index', echo=True)
crawler_engine = create_engine('postgresql+psycopg2://debug:debug\
@crawlerdb/pages', echo=True)