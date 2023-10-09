from flask import Flask
from db import indexer_engine, crawler_engine
from utils import pre_process_query
import pandas as pd

app = Flask(__name__)

@app.route("/hello")
def hello():
    return "hello"


@app.route("/search/<search_string>")
def search(search_string):
    tokens = pre_process_query(search_string)
    dfs = []
    for token in tokens:
        query = f'SELECT page, score FROM "Index" WHERE word = \'{token}\' ORDER BY score LIMIT 10'
        response_df = pd.read_sql_query(query, indexer_engine)
        dfs.append(response_df)
    df = pd.concat(dfs)
    df = df.groupby("page")[["page", "score"]].agg({"score": "sum"})
    df = df.sort_values(by="score", ascending=False)
    df = df.reset_index()
    page_ids = df["page"].values
    if len(page_ids) == 0: return {"message": "No results found"}
    page_ids_str = str(page_ids[0])
    for id in page_ids:
        page_ids_str += f", {id}"
    query = f"SELECT title, description, url FROM page WHERE id IN ({page_ids_str})"
    result_df = pd.read_sql_query(query, crawler_engine)
    results = []
    for title, description, url in zip(result_df["title"].values, result_df["description"].values, result_df["url"].values):
        results.append({"title": title, "description": description, "url": url})
    return results

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8002)