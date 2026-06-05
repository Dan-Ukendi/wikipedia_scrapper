import requests 

class CountryLeadersAPI():
    """
    Client for the Country Leaders REST API.
    Handles cookie management, country listing, and leader fetching.
    """

    def __init__(self):
        """Initialize the API base URL and endpoint paths."""
        self.base_url = "https://country-leaders.onrender.com"
        self.countries_endpoint = "/countries"
        self.leaders_endpoint = "/leaders"
        self.cookies_endpoint = "/cookie"

    def refresh_cookies(self):
        """
        Fetch a fresh session cookie from the API.

        Returns:
            RequestsCookieJar: The cookies returned by the cookie endpoint.
        """
        get_cookies = requests.get(f"{self.base_url}{self.cookies_endpoint}").cookies
        return get_cookies

    def get_countries(self):
        """
        Retrieve the list of supported country codes from the API.

        Returns:
            list[str]: A list of country code strings (e.g. ["be", "fr", "us"]).
        """
        countries = requests.get(
            f"{self.base_url}{self.countries_endpoint}",
            cookies=self.refresh_cookies()
        ).json()
        return countries

    def get_leaders(self):
        """
        Retrieve all political leaders grouped by country.

        Fetches a fresh cookie, gets the country list, then queries the leaders
        endpoint once per country using a dict comprehension.

        Note: the countries request is currently duplicated — one of the two
        lines can be removed.

        Returns:
            dict[str, list]: A dictionary mapping each country code to its
            list of leader objects (as returned by the API).
        """
        root_url = "https://country-leaders.onrender.com"
        countries_url = f"{root_url}/countries"
        leaders_url = f"{root_url}/leaders"
        cookie_url = f"{root_url}/cookie"

        # Get a session cookie required for all subsequent requests
        cookies = requests.get(cookie_url).cookies

        # Fetch the list of country codes (duplicated line — one can be removed)
        countries = requests.get(countries_url, cookies=cookies).json()
        countries = requests.get(countries_url, cookies=cookies).json()

        # Build a dict: { country_code: [leader, ...] } in a single pass
        leaders_per_country = {
            country: requests.get(
                leaders_url,
                cookies=cookies,
                params={"country": country}
            ).json()
            for country in countries
        }

        return leaders_per_country