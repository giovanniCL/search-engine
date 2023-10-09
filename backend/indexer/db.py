from sqlalchemy import String, Integer, create_engine
from sqlalchemy.orm import mapped_column, DeclarativeBase
import os

HOST = os.environ.get("POSTGRES_HOST")
PORT = os.environ.get("POSTGRES_PORT")
DB = os.environ.get("POSTGRES_DB")
USER = os.environ.get("POSTGRES_USER")
PASSWORD = os.environ.get("POSTGRES_PASSWORD")

connection_string = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"

class Base(DeclarativeBase):
    pass

class WordXPage(Base):
    __tablename__ = "Index"
    word = mapped_column(String(100), primary_key=True)
    page = mapped_column(Integer(), primary_key=True)
    score = mapped_column(Integer())

# engine = create_engine(f'postgresql+psycopg2://debug:debug\
# @indexerdb:5433/index', echo=True)
engine = create_engine(connection_string, echo=True)

Base.metadata.create_all(engine)