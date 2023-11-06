SCORE_THRESHOLD = 10
class Indexer:
    def __init__(self, scorer, db_client):
        self.scorer = scorer
        self.db_client = db_client
    
    def index_page(self, id, title, h1, description, text):
        scores = self.scorer.score(text, title, h1, description)
        for word, score in scores.items():
            if score >= SCORE_THRESHOLD:
                self.db_client.create_or_update_index(word, id, score)