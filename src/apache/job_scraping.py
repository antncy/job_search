from dotenv import load_dotenv
from tqdm.asyncio import tqdm
from src.scrapers import LinkedInScraper
from src.tools.job_relevancy import check_job_relevancy
from src.tools.database_access import create_connection, write_to_db, close_connection

load_dotenv()

async def scrape_and_save_jobs(job_title: str, location: str, appear_time: int, max_jobs: int=50, other_job_filters: str=""):
    """
    Scrape job listings from LinkedIn base on provided keywords, location, and appearance time.
    The results are saved to the database.

    Args:
        job_title (str): Job Title to search for in jobs listings.
        location (str): Location to filter job listings.
        appear_time (int): Time frame in hours for job appearance (e.g., last 24 hours).
        max_jobs (int, optional): Maximun number of jobs to scrape.
        other_job_filters (str, optional): Additional filters for job search.
        """
    params = {
        "keywords": "AI Engineer",
        "location": "Paris",
        "appear_time": "r10800",
        "max_jobs": max_jobs,
    }

    scraper = LinkedInScraper.LinkedInJobsScrapper()
    jobs = scraper.scrape_jobs(**params)

    filtered_jobs = []
    tasks = [check_job_relevancy(job, other_job_filters) for job in jobs]
    check_results = await tqdm.gather(*tasks, desc="Check job relevancy")

    for job, result in zip(jobs, check_results):
        if result:
            filtered_jobs.append(job)
    scraper.save_results(filtered_jobs)

    # DB load
    conn, cursor = create_connection("embed_test")
    write_to_db(cursor, filtered_jobs)
    conn.commit()
    close_connection(conn, cursor)
    return