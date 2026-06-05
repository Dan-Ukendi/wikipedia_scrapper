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
    
    def get_leaders(self):
        root_url = "https://country-leaders.onrender.com"
        countries_url = f"{root_url}/countries"
        leaders_url = f"{root_url}/leaders"
        cookie_url = f"{root_url}/cookie"
        cookies = requests.get(cookie_url).cookies 
        countries = requests.get(countries_url, cookies=cookies).json()  
        countries = requests.get(countries_url, cookies=cookies).json()

        leaders_per_country = {country: requests.get(leaders_url, cookies=cookies, params={"country": country}).json() for country in countries}


        return leaders_per_country

test = CountryLeadersAPI()