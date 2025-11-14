import os
import asyncio

from dotenv import load_dotenv
from src.tools.llm_query import llm_retrieve
from src.scrapper.JobData import JobData

load_dotenv()

async def check_job_relevancy(job: JobData, job_requirements: str):
    prompt = f"""
    Given the following job description and job requirements, determine if the job is relevant to the requirements.

    Job Description:
    {job.job_description}

    Job Requirements:
    {job_requirements}

    Answer with "True" or "False" only.
    """

    response = await llm_retrieve(prompt)
    return response.strip().lower() == "true"