import requests
from db import Page, engine
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
import os
from scraper import Scraper
from sqlalchemy_client import SqlAlchemyClient

INDEXER_URL = os.environ.get("INDEXER_URL")

queue = ["https://www.reddit.com/"]
visited = set("https://www.reddit.com/")
count = 0
db_client = SqlAlchemyClient(engine, Page)
while count < 1000 and len(queue) > 0:
    site_url = queue.pop()
    try:
        result = requests.get(site_url)
    except requests.exceptions.InvalidSchema:
        continue
    except:
        continue
    if result.status_code // 100 != 2: continue
    scraper = Scraper(result)
    if scraper.lang_code is None or not (scraper.lang_code.startswith("en") or scraper.lang_code.startswith("es")): continue
    parsed_site = scraper.to_dict()
    inserted_id = db_client.create_or_update_page(parsed_site)
    for link in scraper.get_urls():
        if link and link not in visited and link.startswith("http") and len(link) <= 100:
            queue.append(link)
            visited.add(link)
    try:
        response = requests.post(INDEXER_URL, json={"id": inserted_id, "title": scraper.title, "text": scraper.text})
    except Exception as e:
        print(e)
    count += 1