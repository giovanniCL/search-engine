class Indexer:
    def __init__(self, scorer, db_client):
        self.scorer = scorer
        self.db_client = db_client
    
    def index_page(self, id, title, text):
        scores = self.scorer.score(text, title)
        for word, score in scores.items():
            self.db_client.create_or_update_index(word, id, score)