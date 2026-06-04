from src.api_client import CountryLeadersAPI
from src.HTML_Scraper import wikipedia_scrapper
from src.HTML_Scraper import create_session

def main():
    api = CountryLeadersAPI()
    session = create_session()
    scrapper = wikipedia_scrapper(session)
    leaders_per_country = api.get_leaders()
    if leaders_per_country:
        for contries in leaders_per_country:
            for leader in contries:
                leader["Bio"] = scrapper.get_first_paragraphe(leader[wiki])
        for leader in leaders_per_country:
            print(leader["Bio"])
main()
