from src.api_client import CountryLeadersAPI
from src.HTML_Scraper import wikipedia_scrapper
from src.HTML_Scraper import create_session
from threading import Thread, RLock
from time import sleep


class Search(Thread):
    """
    Worker thread that scrapes Wikipedia bios for all leaders of one country.

    Each instance is responsible for a single country. It iterates over the
    leaders list, fetches the first Wikipedia paragraph for each, and writes
    the result back into the shared `leaders_per_country` dict under the
    key "Bio".

    A class-level RLock ensures that concurrent writes to the shared dict
    are thread-safe.
    """

    # Shared reentrant lock — one instance used by all Search threads
    lock = RLock()

    def __init__(self, country, leaders_per_country, scrapper):
        """
        Args:
            country (str): The country code this thread will process (e.g. "be").
            leaders_per_country (dict): Shared dict mapping country codes to leader lists.
            scrapper (wikipedia_scrapper): Shared scraper instance with an active session.
        """
        super().__init__()
        self.country = country
        self.leaders_per_country = leaders_per_country
        self.scrapper = scrapper

    def run(self):
        """
        Thread entry point.

        For each leader in the assigned country:
        1. Reads their wikipedia_url.
        2. Calls the scraper to get the first biographical paragraph.
        3. Waits 100 ms to avoid hammering Wikipedia's servers.
        4. Acquires the lock and writes the result to the leader dict.
        """
        for leader in self.leaders_per_country[self.country]:
            url = leader["wikipedia_url"]
            first_para = self.scrapper.get_first_paragraphe(url, self.leaders_per_country)
            sleep(.1)  # Polite delay between requests
            with self.lock:
                # Write result inside the lock to prevent race conditions
                leader["Bio"] = first_para


def main():
    """
    Pipeline entry point.

    Steps:
    1. Instantiate the API client and fetch all leaders per country.
    2. Create a shared HTTP session and scraper.
    3. Spawn one Search thread per country and run them concurrently.
    4. Wait for all threads to finish, then save the enriched dataset to JSON.
    """
    # --- Setup ---
    api = CountryLeadersAPI()
    session = create_session()
    scrapper = wikipedia_scrapper(session.session)

    # Fetch the full leaders dataset from the API
    leaders_per_country = api.get_leaders()

    if leaders_per_country:
        # --- Spawn one thread per country ---
        threads = []
        for country in leaders_per_country:
            threads.append(Search(country, leaders_per_country, scrapper))

        # Start all threads
        for thread in threads:
            thread.start()

        # Wait for all threads to complete before saving
        for thread in threads:
            thread.join()

    # --- Persist results ---
    scrapper.save(leaders_per_country, "leaders.json")


main()