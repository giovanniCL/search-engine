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

class Page(Base):
    __tablename__ = "page"
    id = mapped_column(Integer(), primary_key=True, autoincrement=True)
    url = mapped_column(String(100), unique=True)
    title = mapped_column(String(280))
    h1 = mapped_column(String(280))
    description = mapped_column(String(280))

engine = create_engine(connection_string, echo=True)

Base.metadata.create_all(engine)