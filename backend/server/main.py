from flask import Flask
from db import indexer_engine, crawler_engine
from utils import pre_process_query
from sqlalchemy_pandas_client import SqlAlchemyPandasClient

db_client = SqlAlchemyPandasClient(indexer_engine, crawler_engine)

app = Flask(__name__)

@app.route("/search/<search_string>")
def search(search_string):
    tokens = pre_process_query(search_string)
    page_ids = db_client.get_page_ids(tokens)
    if len(page_ids) == 0: return {"message": "No results found"}, 404
    results = db_client.get_results(page_ids)
    return results, 200

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8002)