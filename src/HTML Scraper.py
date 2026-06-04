import requests
from bs4 import BeautifulSoup

class create_session ():
    def __init__(self):
        request_session = requests.Session()
        request_session.headers.update({
        "User-Agent": "wikibecode (danukendi1@gmail.com)"
    })
        self.session = request_session

import re
def clean(text):
    text = re.sub(r'\[[^\]]{1,30}\]|[ⓘ©®™°•·]', '', text)
    text = re.sub(r'[^\w\s\.\,\:\;\!\?\-–—\'\"\(\)\n]', '', text, flags=re.UNICODE)
    return re.sub(r' +|\n+', lambda m: ' ' if ' ' in m.group() else '\n', text).strip()

def name(wikipedia_url, leaders_per_country):
    for contries in leaders_per_country:
        for leader in leaders_per_country[contries]:
            if leader["wikipedia_url"] == wikipedia_url:
                return leader["first_name"]  +" "+ leader["last_name"]

def get_first_paragraph(wikipedia_url, session, leaders_per_country):
     response = session.get(wikipedia_url)
     soup = BeautifulSoup(response.text, "html.parser")
     for p in soup.find_all("p"):
        if p.text.startswith(name(wikipedia_url, leaders_per_country)):
            return clean(p.text)


def wikipedia_scrapper(url, session):
    texte = ""
    response = session.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    for p in soup.find_all("p"):
        texte += clean(p.text)
    return (texte)

