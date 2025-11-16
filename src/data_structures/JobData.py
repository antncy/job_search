from dataclasses import dataclass

@dataclass
class JobData:
    title: str
    company: str
    location: str
    job_link: str
    posted_date: str
    job_description: str = ""
    # To add additional fields (easy_apply, seniority level, employment_type, job_function)
