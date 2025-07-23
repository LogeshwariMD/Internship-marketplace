import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time


headers = {
    'User-Agent': 'Mozilla/5.0'
}


base_url = "https://www.linkedin.com/jobs/search/?keywords=internship&location=India&start="


data = []


for start in range(0, 200, 25):
    url = base_url + str(start)
    print(f"Fetching page with start offset: {start}")
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error fetching URL: {url}; Status Code: {response.status_code}")
        continue

    soup = BeautifulSoup(response.text, 'html.parser')

    
    jobs = soup.find_all('div', class_='base-card')

    if not jobs:
        print(f"No jobs found on page with start offset: {start}")
        continue

    
    for job in jobs:
        
        try:
            job_title = job.find('h3', class_='base-search-card__title').text.strip()
        except Exception:
            job_title = "No Title Found"

        
        try:
            company_name = job.find('h4', class_='base-search-card__subtitle').text.strip()
        except Exception:
            company_name = "No Company Found"

        
        try:
            location = job.find('span', class_='job-search-card__location').text.strip()
        except Exception:
            location = "Not specified"

    
        try:
            time_tag = job.find('time')
            posted_date = time_tag.get('datetime') if time_tag and time_tag.get('datetime') else datetime.now().strftime("%Y-%m-%d")
        except Exception:
            posted_date = datetime.now().strftime("%Y-%m-%d")

        
        platform = "LinkedIn"
        domain_category = "Not specified"     
        skills_required = "Not provided"
        stipend = "Not specified"
        duration_months = "Not specified"
        intern_type = "Not specified"


        record = [
            platform,
            company_name,
            job_title,
            domain_category,
            skills_required,
            location,
            stipend,
            duration_months,
            posted_date,
            intern_type
        ]
        data.append(record)

    
    if len(data) >= 200:
        print(f"Collected {len(data)} records so far. Stopping pagination.")
        break

    
    time.sleep(1)


data = data[:200]


columns = [
    "platform", "company_name", "job_title", "domain_category",
    "skills_required", "location", "stipend", "duration_months",
    "posted_date", "intern_type"
]
df = pd.DataFrame(data, columns=columns)


print(df.head())
print(f"Total records scraped: {len(df)}")


df.to_csv("linkedin_internship_data.csv", index=False)
print("Data saved to linkedin_internship_data.csv")
