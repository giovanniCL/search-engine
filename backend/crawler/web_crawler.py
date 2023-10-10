import requests
class WebCrawler:
    def __init__(self, seed_pages, scraper_class, db_client, indexer_client, n_iters=None, languages=None):
        self.queue = seed_pages
        self.visited = set(self.queue)
        self.scraper_class = scraper_class
        self.db_client = db_client
        self.indexer_client = indexer_client
        self.n_iters = n_iters if n_iters is not None else float("inf")
        self.languages = languages if languages is not None else ["en", "es"]

    def crawl(self):
        count = 0
        while count < self.n_iters and len(self.queue) > 0:
            site_url = self.queue.pop()
            try:
                result = requests.get(site_url)
            except requests.exceptions.InvalidSchema:
                continue
            except:
                continue
            if result.status_code // 100 != 2: continue
            scraper = self.scraper_class(result)
            if not self.validate_language(scraper.lang_code): continue
            parsed_site = scraper.to_dict()
            inserted_id = self.db_client.create_or_update_page(parsed_site)
            self.indexer_client.index_page(inserted_id, scraper)
            for link in scraper.get_urls():
                if self.validate_url(link):
                    self.queue.append(link)
                    self.visited.add(link)    
            count += 1

    def validate_language(self, lang_code):
        if lang_code is None: return False
        for language in self.languages:
            if lang_code.startswith(language): return True
        return False
    
    def validate_url(self, url):
        if url is None: return False
        if url in self.visited: return False
        if not url.startswith("http"): return False
        return len(url) <= 100