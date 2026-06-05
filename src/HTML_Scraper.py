import requests
from bs4 import BeautifulSoup
import re
import json
import os


class create_session:
    """
    Factory class that creates and configures a persistent requests.Session.
    Sets a descriptive User-Agent header as required by Wikipedia's API policy.
    """

    def __init__(self):
        """Create a session and attach a User-Agent header to all requests."""
        request_session = requests.Session()
        request_session.headers.update({
            "User-Agent": "wikibecode (danukendi1@gmail.com)"
        })
        self.session = request_session


def clean(text):
    """
    Sanitize a raw Wikipedia paragraph.

    Removes:
    - Citation brackets like [1], [note], [citation needed]
    - Special Unicode symbols (ⓘ, ©, ®, ™, etc.)
    - Any character that is not a word character, standard punctuation, or whitespace
    - Consecutive spaces and blank lines

    Args:
        text (str): Raw paragraph text extracted from HTML.

    Returns:
        str: Cleaned plain text.
    """
    # Remove citation brackets (e.g. [1], [note]) and stray symbols
    text = re.sub(r'\[[^\]]{1,30}\]|[ⓘ©®™°•·]', '', text)
    # Keep only word characters, standard punctuation and whitespace
    text = re.sub(r'[^\w\s\.\,\:\;\!\?\-–—\'\"\(\)\n]', '', text, flags=re.UNICODE)
    # Collapse multiple spaces into one, multiple newlines into one
    return re.sub(r' +|\n+', lambda m: ' ' if ' ' in m.group() else '\n', text).strip()


def date(wikipedia_url, leaders_per_country):
    """
    Find a reliable year string to anchor paragraph detection for a given leader.

    Looks up the leader whose wikipedia_url matches, then returns:
    - Their birth year (first 4 chars of birth_date) if available
    - Their end_mandate year for a specific edge case (Mohammed, mandate ended 1517)
    - Their first name as a fallback when no date is found

    Args:
        wikipedia_url (str): The Wikipedia URL of the leader to look up.
        leaders_per_country (dict): The full leaders dataset keyed by country code.

    Returns:
        str | None: A year string (e.g. "1962") or first name, or None if not found.
    """
    for contries in leaders_per_country:
        for chef in leaders_per_country[contries]:
            if chef["wikipedia_url"] == wikipedia_url:
                if chef["birth_date"]:
                    # Use the 4-digit birth year
                    return chef["birth_date"][0:4]
                elif chef["first_name"] == "Mohammed" and chef["end_mandate"] == "1517-01-01":
                    # Edge case: historical figure with no birth date
                    return chef["end_mandate"][0:4]
                else:
                    # Last resort: use the first name to search the paragraph
                    return chef["first_name"]


class wikipedia_scrapper:
    """
    Scraper that downloads Wikipedia pages and extracts the first
    biographical paragraph for a given leader.
    """

    def __init__(self, session) -> None:
        """
        Args:
            session (requests.Session): A configured session (from create_session).
        """
        self.session = session

    def fetch_url(self, url):
        """
        Download the HTML content of a URL.

        Handles common network errors gracefully by printing a message
        and returning None instead of raising.

        Args:
            url (str): The page URL to fetch.

        Returns:
            str | None: Raw HTML text, or None on failure.
        """
        try:
            response = self.session.get(url)
            return response.text
        except ConnectionError:
            print("no connection")
        except TimeoutError:
            print("Time out")
        except Exception:
            print("ERROR")

    def get_first_paragraphe(self, url, leaders_per_country):
        """
        Fetch a Wikipedia page and return the first paragraph that contains
        the leader's identifying year (or name).

        Uses the `date()` helper to find a string that should appear in the
        introductory paragraph (typically the birth year), then searches all
        <p> tags until a match is found.

        Args:
            url (str): Wikipedia URL for the leader.
            leaders_per_country (dict): Full leaders dataset (needed by `date()`).

        Returns:
            str | None: Cleaned first paragraph text, or None if not found.
        """
        response = self.fetch_url(url)
        if not response:
            return None

        soup = BeautifulSoup(response, "html.parser")
        year = date(url, leaders_per_country)

        if year is None:
            print("Error info")
            return None

        # Walk all <p> tags and return the first one containing the anchor string
        for p in soup.find_all("p"):
            text = str(p.text)
            if year in text:
                return clean(text)

    def save(self, leaders_per_country, filename="leaders.json"):
        """
        Serialize the leaders dataset to a JSON file.

        The file is saved in the same directory as this script.

        Args:
            leaders_per_country (dict): The full leaders dataset to persist.
            filename (str): Output filename (default: "leaders.json").
        """
        script_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(script_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(leaders_per_country, f, ensure_ascii=False, indent=4)


# ---------------------------------------------------------------------------
# Standalone helper (duplicates CountryLeadersAPI.get_leaders — kept for now)
# ---------------------------------------------------------------------------

def get_leaders():
    """
    Fetch all leaders grouped by country directly (without the API class).

    Note: this function duplicates logic already in CountryLeadersAPI.get_leaders().
    Consider removing it and using the class instead.

    Returns:
        dict[str, list]: Leaders per country code.
    """
    root_url = "https://country-leaders.onrender.com"
    countries_url = f"{root_url}/countries"
    leaders_url = f"{root_url}/leaders"
    cookie_url = f"{root_url}/cookie"

    cookies = requests.get(cookie_url).cookies
    # Note: countries is fetched twice here — one line can be removed
    countries = requests.get(countries_url, cookies=cookies).json()
    countries = requests.get(countries_url, cookies=cookies).json()

    leaders_per_country = {
        country: requests.get(
            leaders_url,
            cookies=cookies,
            params={"country": country}
        ).json()
        for country in countries
    }

    return leaders_per_country


# Module-level calls below run on import — consider moving them into a
# if __name__ == "__main__" block or into main.py to avoid side effects.
leaders_per_country = get_leaders()
session = create_session()
wiki_scrap = wikipedia_scrapper(session.session)