import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

def scrape_rozee_jobs(keyword="software engineer", pages=2):
    jobs = []
    for page in range(1, pages + 1):
        url = f"https://www.rozee.pk/job/jsearch/q/{keyword}/p/{page}"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "lxml")

        listings = soup.find_all("div", class_="job")

        for listing in listings:
            title = listing.find("a", class_="job-title").text.strip() if listing.find("a", class_="job-title") else "N/A"
            company = listing.find("span", class_="company-name").text.strip() if listing.find("span", class_="company-name") else "N/A"
            location = listing.find("span", class_="job-location").text.strip() if listing.find("span", class_="job-location") else "N/A"
            skills = ', '.join([tag.text.strip() for tag in listing.find_all("a", class_="job-tag")]) if listing.find_all("a", class_="job-tag") else "N/A"
            date_posted = listing.find("span", class_="job-date").text.strip() if listing.find("span", class_="job-date") else "N/A"

            jobs.append({
                "Title": title,
                "Company": company,
                "Location": location,
                "Skills": skills,
                "Date Posted": date_posted
            })

        time.sleep(1)  # Polite delay to avoid hammering the server

    return jobs


if __name__ == "__main__":
    keyword = "data analyst"
    data = scrape_rozee_jobs(keyword=keyword, pages=3)

    df = pd.DataFrame(data)
    df.to_csv("job_data_rozee.csv", index=False)
    print("✅ Scraping completed. Data saved to job_data_rozee.csv")
