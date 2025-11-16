from typing import List, Optional
from bs4 import BeautifulSoup
from loguru import logger
from src.data_structures.JobData import JobData
from src.data_structures.ScraperConfig import ScraperConfig
from src.scrapers.JobsScraper import JobScraper
import aiohttp
import json

class LinkedInJobsScrapper(JobScraper):
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"

    def _extract_job_data(self, job_card: BeautifulSoup) -> Optional[JobData]:
        """Extract job data from a job card."""
        try:
            title = job_card.find("h3", class_="base-search-card__title").text.strip()
            company = job_card.find(
                "h4", class_="base-search-card__subtitle"
            ).text.strip()
            location = job_card.find(
                "span", class_="job-search-card__location"
            ).text.strip()
            job_link = self._clean_job_url(
                job_card.find("a", class_="base-card__full-link")["href"]
            )
            posted_date = job_card.find("time", class_="job-search-card__listdate")
            posted_date = posted_date.text.strip() if posted_date else "N/A"
            job_discription = self._get_job_description(job_link)

            return JobData(
                title=title,
                company=company,
                location=location,
                job_link=job_link,
                posted_date=posted_date,
                job_description=job_discription
            )
        except Exception as e:
            logger.error(f"Failed to extract job data: {str(e)}")
            return None

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


    def _get_job_description(self, job_url: str) -> str:
        job_page_soup = self._fetch_job_page(job_url)
        job_description_section = job_page_soup.find("section", class_="show-more-less-html")
        if job_description_section:
            job_description = job_description_section.get_text(strip=True)
            job_description = job_description.replace("Show moreShow less", "").strip()
        else:
            job_description = "N/A"
        return job_description
    
    def scrape_jobs(self, keywords: str, location: str, appear_time: str, max_jobs: int=50) -> List[JobData]:
        all_jobs = []
        start = 0

        while len(all_jobs) < max_jobs:
            try:
                url = self._build_search_url(keywords, location, appear_time, start)
                soup = self._fetch_job_page(url)
                job_cards = soup.find_all("div", class_="base-card")
                if not job_cards:
                    break
                

                for job_card in job_cards:
                    all_jobs.append(self._extract_job_data(job_card))
                
                start += ScraperConfig.JOBS_PER_PAGE
            except Exception as e:
                logger.error(f"Scrapping error: {str(e)}")
                break
        return all_jobs[:max_jobs]
    
    def save_results(
        self, jobs: List[JobData], filename: str="linkedin_jobs.json" 
    ) -> None:
        if not jobs:
            return
        with open(filename, "w", encoding="utf-8") as f:
            json.dump([vars(job) for job in jobs], f, ensure_ascii=False, indent=2)

def main():
    params = {
        "keywords": "Data Scientist",
        "location": "Paris",
        "appear_time": "r3600", # last 24 hours
        "max_jobs": 20,
    }

    scraper = LinkedInJobsScrapper()
    jobs = scraper.scrape_jobs(**params)
    scraper.save_results(jobs)

if __name__ == "__main__":
    main()