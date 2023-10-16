import requests

class IndexerClient:
    def __init__(self, url):
        self.url = url

    def index_page(self, id, scraped_page):
        json_body = {
            "id": id,
            "title": scraped_page.title,
            "h1": scraped_page.h1,
            "description": scraped_page.description,
            "text": scraped_page.text
        }
        try:
            response = requests.post(self.url,json=json_body)
        except Exception as e:
            print("Error while trying to index page:")
            print(e)