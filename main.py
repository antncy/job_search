from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from src.scrapper import LinkedInScrapper

load_dotenv()

mcp = FastMCP("Job Scraper MCP")

@mcp.tool()
def scrape_jobs(keywords: str, location: str, appear_time: int, max_jobs: int=50):
    """
    Scrape job listings from LinkedIn base on provided keywords, location, and appearance time.

    Args:
        keywords (str): Keywords to search for in jobs listings.
        location (str): Location to filter job listings.
        appear_time (int): Time frame in hours for job appearance (e.g., last 24 hours).
        max_jobs (int, optional): Maximun number of jobs to scrape.
    
    Returns:
        A list of dictionaries containing job data.
    """
    params = {
        "keywords": keywords,
        "location": location,
        "appear_time": "r" + str(3600 * appear_time), # last 24 hours
        "max_jobs": max_jobs,
    }

    scraper = LinkedInScrapper.LinkedInJobsScrapper()
    jobs = scraper.scrape_jobs(**params)
    scraper.save_results(jobs)

    return [vars(job) for job in jobs]

if __name__ == "__main__":
    mcp.run(transport="stdio")

