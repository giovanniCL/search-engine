from bs4 import BeautifulSoup
from utils.utils import pre_process_text

class Scraper:
    def __init__(self, response):
        self.url = response.url if not response.history else response.history[0].url
        self.soup = BeautifulSoup(response.content, 'html.parser')
        self.lang_code = self.soup.html.get("lang")
        self.set_title()
        self.set_description_meta()
        self.set_h1()
        self.set_h2()
        self.set_first_p()
        self.set_description()
        self.text = self.soup.get_text()

    def set_title(self):
        self.title = "" if not self.soup.title else self.soup.title.string

    def set_description_meta(self):
        description_meta = self.soup.find("meta", {"name":"description"})
        self.description_meta = None if not description_meta else description_meta.get("content")

    def set_h1(self):
        h1 = self.soup.find("h1")
        self.h1 = None if not h1 else h1.text

    def set_h2(self):
        h2 = self.soup.find("h2")
        self.h2 = None if not h2 else h2.text

    def set_first_p(self):
        first_p = self.soup.find('p')
        self.first_p = None if not first_p else first_p.text

    def set_description(self):
        self.description = self.description_meta if self.description_meta else (self.h2 if self.h2 else self.first_p)

    def get_urls(self):
        urls = []
        for anchor in self.soup.find_all('a'):
            urls.append(anchor.get('href'))
        return urls

    def to_dict(self):
        return {
            "url": self.url,
            "title": pre_process_text(self.title, max_len=280),
            "h1": pre_process_text(self.h1, max_len=280),
            "description": pre_process_text(self.description, max_len=280)
        }

    