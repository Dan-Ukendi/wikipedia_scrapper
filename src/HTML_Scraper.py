import requests
from bs4 import BeautifulSoup
import re
import json
import os


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

def date(wikipedia_url,leaders_per_country):
    for contries in leaders_per_country:
        for chef in leaders_per_country[contries]:
            if chef["wikipedia_url"] == wikipedia_url:
                if chef["birth_date"]:
                    return chef["birth_date"][0:4]
                elif chef["first_name"] == "Mohammed" and chef["end_mandate"] == "1517-01-01":
                    return chef["end_mandate"][0:4]
                else :
                    return chef["first_name"]

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
    
    def get_first_paragraphe(self,url,leaders_per_country):
        response = self.fetch_url(url)
        if not response:
            return None
        soup = BeautifulSoup(response, "html.parser")
        year = date(url,leaders_per_country)
        if year is None:
            print("Error info")
            return None
        for p in soup.find_all("p"):
            text = str(p.text)
            if  year in text:
                return clean(text)

    def save(self, leaders_per_country, filename="leaders.json"):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(script_dir, filename)
    
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(leaders_per_country, f, ensure_ascii=False,indent = 4)
    
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