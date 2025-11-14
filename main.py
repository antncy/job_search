import os
import asyncio

from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from src.scrapper import LinkedInScrapper
from src.tools.job_relevancy import check_job_relevancy

load_dotenv()

mcp = FastMCP("Job Scraper MCP")

@mcp.tool()
async def scrape_jobs(job_title: str, location: str, appear_time: int, max_jobs: int=50, other_job_filters: str=""):
    """
    Scrape job listings from LinkedIn base on provided keywords, location, and appearance time.

    Args:
        job_title (str): Job Title to search for in jobs listings.
        location (str): Location to filter job listings.
        appear_time (int): Time frame in hours for job appearance (e.g., last 24 hours).
        max_jobs (int, optional): Maximun number of jobs to scrape.
        other_job_filters (str, optional): Additional filters for job search.
    
    Returns:
        A list of dictionaries containing job data.
    """
    params = {
        "keywords": job_title,
        "location": location,
        "appear_time": "r" + str(3600 * appear_time), # last 24 hours
        "max_jobs": max_jobs,
    }

    scraper = LinkedInScrapper.LinkedInJobsScrapper()
    jobs = scraper.scrape_jobs(**params)

    filtered_jobs = []
    for job in jobs:
        is_relevant = await check_job_relevancy(job, other_job_filters)
        if is_relevant:
            filtered_jobs.append(job)
    scraper.save_results(filtered_jobs)

    return [vars(job) for job in filtered_jobs]

if __name__ == "__main__":
    mcp.run(transport="stdio")

