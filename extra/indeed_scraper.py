import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def scrape_indeed_jobs(keyword="data analyst", location="Pakistan", pages=2):
    # base_url = "https://pk.indeed.com/jobs"
    base_url = "https://pk.indeed.com/jobs?q=&l=karachi&from=searchOnHP"
    
    jobs = []

    for page in range(pages):
        params = {
            "q": keyword,
            "l": location,
            "start": page * 10
        }

        response = requests.get(base_url, params=params, headers=headers)
        soup = BeautifulSoup(response.content, "lxml")

        job_cards = soup.find_all("div", class_="job_seen_beacon")

        for card in job_cards:
            title_elem = card.find("h2", class_="jobTitle")
            title = title_elem.text.strip() if title_elem else "N/A"

            company_elem = card.find("span", class_="companyName")
            company = company_elem.text.strip() if company_elem else "N/A"

            location_elem = card.find("div", class_="companyLocation")
            location = location_elem.text.strip() if location_elem else "N/A"

            date_elem = card.find("span", class_="date")
            date_posted = date_elem.text.strip() if date_elem else "N/A"

            snippet_elem = card.find("div", class_="job-snippet")
            snippet = snippet_elem.text.strip().replace('\n', ' ') if snippet_elem else "N/A"

            jobs.append({
                "Title": title,
                "Company": company,
                "Location": location,
                "Skills": snippet,
                "Date Posted": date_posted
            })

        time.sleep(1)  # polite delay

    return jobs


if __name__ == "__main__":
    keyword = "data analyst"
    location = "Pakistan"
    data = scrape_indeed_jobs(keyword=keyword, location=location, pages=3)

    df = pd.DataFrame(data)
    df.to_csv("job_data_indeed.csv", index=False)
    print("✅ Scraping completed. Data saved to job_data_indeed.csv")
