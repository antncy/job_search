import requests

url = "https://fr.linkedin.com/jobs/view/consultant-e-data-scientist-ai-engineer-at-leonar-4335761028"
headers = {
    "Authorization": "Bearer jina_ae21e1932fe0443c93a2ac63e1d0c0e7xf_tv_-9Kk1_MhnXdSoy31BWHOrT"
}

response = requests.get(url, headers=headers)

with open('job_page.html', 'w', encoding='utf-8') as file:
    file.write(response.text)
