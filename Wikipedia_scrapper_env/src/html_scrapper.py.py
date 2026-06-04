import requests
from bs4 import BeautifulSoup
import re

def clean(text):
    text = re.sub(r'\[[^\]]{1,30}\]|[ⓘ©®™°•·]', '', text)
    text = re.sub(r'[^\w\s\.\,\:\;\!\?\-–—\'\"\(\)\n]', '', text, flags=re.UNICODE)
    return re.sub(r' +|\n+', lambda m: ' ' if ' ' in m.group() else '\n', text).strip()

def get_session():
     session = requests.Session()
     session.headers.update({
        "User-Agent": "wikibecode (danukendi1@gmail.com)"
    })
     return session

def get_wikipedia_page_content(url, session):
    paragraphs = ""
    try:
        response = session.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        response.raise_for_status()
        for p in soup.find_all('p'):
            paragraphs += clean(p.get_text()) + "\n"
        return paragraphs
    except requests.RequestException as e:
        print(f"Error fetching the page: {e}")
        return None
     
page = get_wikipedia_page_content("https://en.wikipedia.org/wiki/Fran%C3%A7ois_Mitterrand", get_session())
print(page)
