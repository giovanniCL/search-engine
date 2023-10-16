from flask import Flask
from flask_restful import Api, Resource, reqparse
from db.db import WordXPage, engine
from db.sqlalchemy_client import SqlAlchemyClient
from indexer.web_indexer import Indexer
from indexer.scorer import Scorer

app = Flask(__name__)
api = Api(app)

db_client = SqlAlchemyClient(engine, WordXPage)

indexer = Indexer(Scorer, db_client)

page_args = reqparse.RequestParser()
page_args.add_argument("id", type=int)
page_args.add_argument("title", type=str)
page_args.add_argument("text", type=str)
page_args.add_argument("h1", type=str)
page_args.add_argument("description", type=str)



class Page(Resource):
    def post(self):
        args = page_args.parse_args()
        indexer.index_page(args["id"], args["title"], args["h1"], args["description"], args["text"])

api.add_resource(Page, '/')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8001)
