from src.api_client import CountryLeadersAPI
from src.HTML_Scraper import wikipedia_scrapper
from src.HTML_Scraper import create_session
from threading import Thread
from threading import RLock
from time import sleep

class Search(Thread):
    lock = RLock()

    def __init__(self,contry,leaders_per_country,scrapper):
        super().__init__()
        self.contry = contry
        self.leaders_per_country = leaders_per_country
        self.scrapper = scrapper
    

    def run(self):
        for leader in self.contry:
            url = leader["wikipedia_url"]
            first_para = self.scrapper.get_first_paragraphe(url,self.leaders_per_country)
            sleep(.1)
            with self.lock:
                leader["Bio"] = first_para





def main():
    api = CountryLeadersAPI()
    session = create_session()
    scrapper = wikipedia_scrapper(session.session)
    leaders_per_country = api.get_leaders()
    if leaders_per_country:
        threads = list()
        for contries in leaders_per_country:
            threads.append(Search(contries,leaders_per_country,scrapper))
        for find in threads:
            find.start
        for find in threads:
            find.join 
    scrapper.save(leaders_per_country,"leaders.json")
main()