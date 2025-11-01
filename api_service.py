from typing import Final
import requests


API:Final[str]= "https://ipinfo.io/"
API_KEY:Final[str]= '9187be05321193' 

def get_country(ip: str)->str:
    try:
        url = API + ip + '?token=' + API_KEY
        response = requests.get(url, timeout=4)
        if response.status_code == 200:
            data = response.json()
            country = data.get("country")
            return country
        return ""
    except Exception :
        return ""
    