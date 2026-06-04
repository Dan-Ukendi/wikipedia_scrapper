import requests
from bs4 import BeautifulSoup
import re
import json

class create_session ():
    def __init__(self):
        request_session = requests.Session()
        request_session.headers.update({
        "User-Agent": "wikibecode (danukendi1@gmail.com)"
    })
        self.session = request_session

def clean(text):
    text = re.sub(r'\[[^\]]{1,30}\]|[ⓘ©®™°•·]', '', text)
    text = re.sub(r'[^\w\s\.\,\:\;\!\?\-–—\'\"\(\)\n]', '', text, flags=re.UNICODE)
    return re.sub(r' +|\n+', lambda m: ' ' if ' ' in m.group() else '\n', text).strip()

def date(wikipedia_url):
    for contries in leaders_per_country:
        for chef in leaders_per_country[contries]:
            if chef["wikipedia_url"] == wikipedia_url:
                return chef["birth_date"][0:4]

class wikipedia_scrapper():
    def __init__(self,session) -> None:
        self.session = session

    def fetch_url(self,url):
        try :
            response = self.session.get(url)
            return response.text
        
        except ConnectionError:
            print("no connection")
        except TimeoutError:
            print("Time out")
        except :
            print("ERROR")
    
    def get_first_paragraphe(self,url,raw_text):
        soup = BeautifulSoup(raw_text, "html.parser")
        year = date(url)
        if year is None:
            print("Error info")
            return None
        for p in soup.find_all("p"):
            text = str(p.text)
            if  year in text:
                return clean(text)
    
    def save(self,leaders_per_country, filename="leaders.json"):
        with open(filename, "w") as f:
            json.dump(leaders_per_country, f)
    
def get_leaders():
    root_url = "https://country-leaders.onrender.com"
    countries_url = f"{root_url}/countries"
    leaders_url = f"{root_url}/leaders"
    cookie_url = f"{root_url}/cookie"
    cookies = requests.get(cookie_url).cookies 
    countries = requests.get(countries_url, cookies=cookies).json()  
    countries = requests.get(countries_url, cookies=cookies).json()

    leaders_per_country = {country: requests.get(leaders_url, cookies=cookies, params={"country": country}).json() for country in countries}


    return leaders_per_country

leaders_per_country = get_leaders()
session = create_session()
wiki_scrap = wikipedia_scrapper(session.session)