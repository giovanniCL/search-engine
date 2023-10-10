from bs4 import BeautifulSoup
from utils.utils import pre_process_text

class Scraper:
    def __init__(self, response):
        self.url = response.url if not response.history else response.history[0].url
        self.soup  = BeautifulSoup(response.content, 'html.parser')
        self.lang_code = self.soup.html.get("lang")
        self.title = "" if not self.soup.title else self.soup.title.string
        self.description_meta = self.soup.find("meta", property="og:description")
        self.text = self.soup.get_text()
        self.first_p = self.soup.find('p')
        self.first_p_text = None if not self.first_p else self.first_p.text
        self.description_text = self.first_p_text if not self.description_meta else self.description_meta.content

    def get_urls(self):
        urls = []
        for anchor in self.soup.find_all('a'):
            urls.append(anchor.get('href'))
        return urls

    def to_dict(self):
        return {
            "url": self.url,
            "title": None if not self.title else pre_process_text(self.title, max_len=280),
            "description": pre_process_text(self.description_text, max_len=280)
        }

    