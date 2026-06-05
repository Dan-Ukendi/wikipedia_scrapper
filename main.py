from src.api_client import CountryLeadersAPI
from src.HTML_Scraper import wikipedia_scrapper
from src.HTML_Scraper import create_session

def main():
    api = CountryLeadersAPI()
    session = create_session()
    scrapper = wikipedia_scrapper(session.session)
    leaders_per_country = api.get_leaders()
    if leaders_per_country:
        for contries in leaders_per_country:
            for leader in leaders_per_country[contries]:
                url = leader["wikipedia_url"]
                first_para = scrapper.get_first_paragraphe(url,leaders_per_country)
                leader["Bio"] = first_para
    scrapper.save(leaders_per_country,"leaders.json")
main()

