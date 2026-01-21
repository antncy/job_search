import mysql.connector
from src.data_structures.JobData import JobData

def create_connection(table_name: str) -> tuple: 
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        auth_plugin='mysql_native_password',
        database=table_name
    )
    
    cursor = conn.cursor()
    return conn, cursor

def close_connection(conn, cursor) -> None:
    cursor.close()
    conn.close()

def write_to_db(cursor, data: list[JobData]):
    def clean_posted_date(posted_date):
        from datetime import datetime
        if posted_date == "N/A" or not posted_date:
            return datetime.now().strftime('%Y-%m-%d')  # Use today's date
        return posted_date
    
    def clean_description(description):
        if description == "N/A":
            return ""
        # Truncate to 1000 characters to fit database column
        return description[:1000] if description else ""
    
    cursor.executemany(
        "INSERT INTO jobs_list (title, company, location, job_link, posted_date, job_description, search_date)"
        "VALUES(%s, %s, %s, %s, %s, %s, CURDATE())",
        [(job.title, job.company, job.location, job.job_link, clean_posted_date(job.posted_date), clean_description(job.job_description)) for job in data]
    )

def query_db(cursor, query):
    cursor.execute(query) # "SELECT * FROM jobs_list;"
    results = cursor.fetchall()
    return results

if __name__ == "__main__":
    conn, cursor = create_connection("embed_test")
    sample_data = [
        JobData(
            title = "Software Engineer",
            company ="Tech Corp",
            location = "New York",
            job_link = "abc",
            posted_date = "2024-06-02",
            job_description = "Develop and maintain software applications"
        ),
        JobData(
            title = "Data Scientist",
            company = "Data Inc",
            location = "San Francisco",
            job_link = "bcd",
            posted_date = "2025-01-01",
            job_description = "Analyse and interpret datasets"
        )
    ]
    write_to_db(cursor, sample_data)
    conn.commit()
    results = query_db(cursor, "Select * From jobs_list;")
    for row in results:
        print(row)

    close_connection(conn, cursor)
    
    