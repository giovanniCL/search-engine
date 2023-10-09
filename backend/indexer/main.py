from flask import Flask
from flask_restful import Api, Resource, reqparse
from frequencies import get_word_frequencies
from db import WordXPage, engine
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

app = Flask(__name__)
api = Api(app)

page_args = reqparse.RequestParser()
page_args.add_argument("id", type=int)
page_args.add_argument("title", type=str)
page_args.add_argument("text", type=str)


class Page(Resource):
    def post(self):
        args = page_args.parse_args()
        frequencies = get_word_frequencies(args["text"])
        for word, frequency in frequencies.items():
            score = frequency
            if word in args["title"].lower(): score += 100
            stmt = insert(WordXPage).values(
                word=word, page=args["id"],
                score=score
                ).on_conflict_do_update(
                    index_elements=["word", "page"],
                    set_={"score":score}
                )
            with Session(engine) as session:
                session.execute(stmt)
                session.commit()

api.add_resource(Page, '/')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8001)
