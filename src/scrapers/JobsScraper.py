from typing import Optional
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from urllib3 import Retry
from urllib.parse import quote
from requests.adapters import HTTPAdapter
from src.data_structures.JobData import JobData
from src.data_structures.ScraperConfig import ScraperConfig
import requests
import aiohttp

class JobScraper(ABC):
    """Base class for job scrapers."""
    def __init__(self):
        self.session = self._setup_session()
    
    def _setup_session(self):
        session = requests.Session()
        retries = Retry(
            total=5,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        session.mount("https://", HTTPAdapter(max_retries=retries))

        return session
    def _build_search_url(self, keywords: str, location: str, appear_time: str="r86400", start: int=0) -> str:
        params = {
            "keywords": keywords,
            "location": location,
            "f_TPR": appear_time,
            "start": start,
        }
        # example: "https://www.linkedin.com/jobs/search/?currentJobId=4335420168&distance=25.0&f_TPR=r3600&geoId=105015875&keywords=data%20scientist&origin=JOBS_HOME_KEYWORD_HISTORY"
        return f"{self.base_url}?{'&'.join(f'{k}={quote(str(v))}' for k, v in params.items())}"
    
    def _clean_job_url(self, url: str) -> str:
        return url.split("?")[0] if "?" in url else url
    
    def _fetch_job_page(self, url: str) -> BeautifulSoup:
        """Convert url to plain text, then to BeautifulSoup object."""
        try:
            response = self.session.get(url, headers=ScraperConfig.HEADERS)
            if response.status_code != 200:
                raise RuntimeError(
                    f"Failed to fetch data: Status code {response.status_code}"
                )
            return BeautifulSoup(response.text, "html.parser")
        except aiohttp.ClientError as e:
            raise RuntimeError(f"Request failed: {str(e)}")
    
    @abstractmethod
    def _extract_job_data(self, job_card: BeautifulSoup) -> Optional[JobData]:
        """Abstract method to extract job data from a job card."""
        pass
        