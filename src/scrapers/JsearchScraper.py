from typing import List, Optional
from loguru import logger
from src.data_structures.JobData import JobData
from src.scrapers.JobsScraper import JobScraper
import json

class JsearchJobsScraper(JobScraper):
    def __init__(self):
        super().__init__()
        self.base_url = "https://jsearch.p.rapidapi.com/search"
        self.headers = {
            "x-rapidapi-key": "7d307ec371msh6f2fe7a5538fbb8p1e7303jsnab12c3379413",
            "x-rapidapi-host": "jsearch.p.rapidapi.com",
        }
    
    def _build_query_params(self, keywords: str, location: str, max_job: int, country_code: str="fr", date_posted: str="today") -> dict:
        params = {
            "query": f"{keywords} in {location}",
            "page": "1",
            "num_pages": str(max_job // 10 + 1),
            "country": country_code,
            "date_posted": date_posted,  # "today", "3days", "week", "month", "all"
            "radius": "-1",
            "exclude_job_publishers": "LinkedIn",
        }
        return params
    
    def _extract_job_data(self, job_data: dict) -> Optional[JobData]:
        """Extract job data from a job card."""
        try:
            title = job_data.get("job_title")
            company = job_data.get("employer_name")
            location = job_data.get("job_city")
            job_link = job_data.get("job_apply_link")
            posted_date = job_data.get("job_posted_at_datetime_utc")
            job_discription = job_data.get("job_description")

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
    
    def scrape_jobs(self, keywords: str, location: str, country_code: str="fr", appear_time: str="today", max_jobs: int=50, **kwargs) -> List[JobData]:
        all_jobs = []

        try:
            params = self._build_query_params(
                keywords, location, max_jobs, country_code, date_posted=appear_time
            )
            response = self.session.get(
                self.base_url, headers=self.headers, params=params
            )
            job_datas = response.json().get("data", [])

            for job_data in job_datas:
                all_jobs.append(self._extract_job_data(job_data))
            
        except Exception as e:
            logger.error(f"Scrapping error: {str(e)}")
        return all_jobs[:max_jobs]
    
    def save_results(
        self, jobs: List[JobData], filename: str="jsearch_jobs.json" 
    ) -> None:
        if not jobs:
            return
        with open(filename, "w", encoding="utf-8") as f:
            json.dump([vars(job) for job in jobs], f, ensure_ascii=False, indent=2)

def main():
    params = {
        "keywords": "Data Scientist",
        "location": "Paris",
        "country_code": "fr",
        "appear_time": "today", # last hours
        "max_jobs": 20,
    }

    scraper = JsearchJobsScraper()
    jobs = scraper.scrape_jobs(**params)
    scraper.save_results(jobs)

if __name__ == "__main__":
    main()