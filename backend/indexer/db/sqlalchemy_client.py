from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

class SqlAlchemyClient:
    def __init__(self, engine, table):
        self.engine = engine
        self.table = table

    def create_or_update_index(self, word, page, score):
        stmt = insert(self.table).values(
            word=word, page=page,
            score=score
            ).on_conflict_do_update(
                index_elements=["word", "page"],
                set_={"score":score}
            )
        with Session(self.engine) as session:
            session.execute(stmt)
            session.commit()