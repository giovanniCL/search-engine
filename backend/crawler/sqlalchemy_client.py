from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

class SqlAlchemyClient:
    def __init__(self, engine, table):
        self.engine = engine
        self.table = table

    def create_or_update_page(self, data):
        stmt = insert(self.table).values(**data).on_conflict_do_update(index_elements=["url"], set_=data)
        with Session(self.engine) as session:
            result = session.execute(stmt)
            session.commit()
            return result.inserted_primary_key[0]
