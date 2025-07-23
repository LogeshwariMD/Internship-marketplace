import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime


headers = {
    'User-Agent': 'Mozilla/5.0'
}


url = "https://internshala.com/internships/"

response = requests.get(url, headers=headers)
if response.status_code != 200:
    print("Error fetching Internshala page, status code:", response.status_code)
    exit()

soup = BeautifulSoup(response.text, 'html.parser')


cards = soup.find_all('div', class_='individual_internship')



for card in cards:
    
    platform = "Internshala"
    
    
    try:
        job_title = card.find('a', class_='view_detail_button').text.strip()
    except Exception:
        job_title = "No Title Found"
    
    
    try:
        company_name = card.find('a', class_='company_name').text.strip()
    except Exception:
        company_name = "No Company Found"
    
    
    domain_category = "Not specified"
    
    
    skills_required = "Not provided"
    
    
    try:
        location = card.find('span', class_='location').text.strip()
    except Exception:
        location = "Not specified"
    
    
    try:
        stipend = card.find('span', class_='stipend').text.strip()
    except Exception:
        stipend = "Unpaid"
    
    
    try:
        
        duration_elem = card.find(text=lambda t: t and "month" in t.lower())
        duration_months = duration_elem.strip() if duration_elem else "Not specified"
    except Exception:
        duration_months = "Not specified"
    
    
    posted_date = datetime.now().strftime("%Y-%m-%d")
    
    
    intern_type = "Paid" if "₹" in stipend else "Unpaid"
    
    
    data.append([platform, company_name, job_title, domain_category, 
                 skills_required, location, stipend, duration_months, 
                 posted_date, intern_type])


columns = [
    "platform", "company_name", "job_title", "domain_category", 
    "skills_required", "location", "stipend", "duration_months", 
    "posted_date", "intern_type"
]


df = pd.DataFrame(data, columns=columns)
print(df.head())


df.to_csv("internshala_internship_data.csv", index=False)
print("Data saved to internshala_internship_data.csv")
