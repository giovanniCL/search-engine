import pandas as pd

class SqlAlchemyPandasClient:
    def __init__(self, indexer_engine, crawler_engine):
        self.indexer_engine = indexer_engine
        self.crawler_engine = crawler_engine

    def get_page_ids(self, tokens):
        dfs = []
        for token in tokens:
            query = f'SELECT page, score FROM "Index" WHERE word = \'{token}\' ORDER BY score LIMIT 10'
            response_df = pd.read_sql_query(query, self.indexer_engine)
            dfs.append(response_df)
        df = pd.concat(dfs)
        df = df.groupby("page")[["page", "score"]].agg({"score": "sum"})
        df = df.sort_values(by="score", ascending=False)
        df = df.reset_index()
        page_ids = df["page"].values

        return page_ids
    
    def get_results(self, page_ids):
        page_ids_str = str(page_ids[0])
        for id in page_ids:
            page_ids_str += f", {id}"
            query = f"SELECT title, description, url FROM page WHERE id IN ({page_ids_str})"
            result_df = pd.read_sql_query(query, self.crawler_engine)
            results = []
            for title, description, url in zip(result_df["title"].values, result_df["description"].values, result_df["url"].values):
                results.append({"title": title, "description": description, "url": url})
                
        return results