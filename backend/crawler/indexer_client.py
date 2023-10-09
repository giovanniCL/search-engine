import requests

class IndexerClient:
    def __init__(self, url):
        self.url = url

    def index_page(self, id, scraped_page):
        try:
            response = requests.post(self.url, json={"id": id, "title": scraped_page.title, "text": scraped_page.text})
        except Exception as e:
            print("Error while trying to index page:")
            print(e)