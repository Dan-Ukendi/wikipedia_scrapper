import requests 

class CountryLeadersAPI():
    def __init__(self):
        self.base_url = "https://country-leaders.onrender.com"
        self.countries_endpoint = "/countries"
        self.leaders_endpoint = "/leaders"
        self.cookies_endpoint = "/cookie"
        
        
    def refresh_cookies(self):
        get_cookies = requests.get(f"{self.base_url}{self.cookies_endpoint}").cookies
        return get_cookies
    
    def get_countries(self):
        countries = requests.get(f"{self.base_url}{self.countries_endpoint}" , cookies = self.refresh_cookies()).json()
        return countries
    
    def get_leaders(self, country = str):
        try:
            params = {
                "country" : country
            }
            leaders = requests.get(f"{self.base_url}{self.leaders_endpoint}", params, cookies = self.refresh_cookies()).json()
            return leaders
        except:     
            print("Choose a country between : 'fr', 'us', 'be', 'ma', 'ru'")

test = CountryLeadersAPI()