from typing import Final
from dotenv import load_dotenv
import os 
import requests

load_dotenv()

API:Final[str]= "https://ipinfo.io/"
API_KEY = os.getenv("API_KEY") or ""

def get_country(ip: str)->str:
    try:
        url = API + ip + '?token=' + API_KEY
        print(url)
        response = requests.get(url, timeout=4)
        if response.status_code == 200:
            data = response.json()
            country = data.get("country")
            return country
        return ""
    except Exception :
        return ""
    