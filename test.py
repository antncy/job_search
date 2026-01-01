import requests
from urllib3 import Retry
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup


url = "https://www.welcomekit.co/api/v1/external/jobs/all"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "DNT": "1",
    "Cache-Control": "no-cache",
}

session = requests.Session()
retries = Retry(
    total=5,
    backoff_factor=0.5,
    status_forcelist=[429, 500, 502, 503, 504]
)
session.mount("https://", HTTPAdapter(max_retries=retries))
response = session.get(url, headers = HEADERS)

print(response.text)
soup = BeautifulSoup(response.text, "html.parser")

