from bs4 import BeautifulSoup
import requests
from db import Page, engine
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
from utils import pre_process_text
import os

INDEXER_URL = os.environ.get("INDEXER_URL")

queue = ["https://www.reddit.com/"]
visited = set("https://www.reddit.com/")
count = 0
while count < 1000 and len(queue) > 0:
    site_url = queue.pop()
    try:
        result = requests.get(site_url)
    except requests.exceptions.InvalidSchema:
        continue
    except:
        continue
    if result.status_code // 100 != 2: continue
    content = result.content
    soup = BeautifulSoup(content, 'html.parser')
    lang_code = soup.html.get("lang")
    if lang_code is None or not (lang_code.startswith("en") or lang_code.startswith("es")): continue
    title = soup.title
    description = soup.find("meta", property="og:description")
    text = soup.get_text()
    first_p = soup.find('p')
    first_p = None if not first_p else first_p.text
    description = first_p if not description else description.content
    parsed_site = {
        "url": site_url, 
        "title": None if not title else pre_process_text(title.string, max_len=280),
        "description": pre_process_text(description, max_len=280)
    }
    stmt = insert(Page).values(**parsed_site).on_conflict_do_update(index_elements=["url"], set_=parsed_site)
    with Session(engine) as session:
        result = session.execute(stmt)
        session.commit()
        inserted_id = result.inserted_primary_key[0]
    for anchor in soup.find_all('a'):
        link = anchor.get('href')
        if link and link not in visited and link.startswith("http") and len(link) <= 100:
            queue.append(link)
            visited.add(link)
    try:
        response = requests.post(INDEXER_URL, json={"id": inserted_id, "title": parsed_site["title"], "text": text})
    except Exception as e:
        print(e)
    count += 1