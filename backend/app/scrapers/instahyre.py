from typing import Any, Dict, List
import httpx
from bs4 import BeautifulSoup
from app.scrapers.base import BaseScraper
from app.scrapers.common import dedupe_jobs, is_design_related, normalize_job

class InstahyreScraper(BaseScraper):
    """
    Scraper for Instahyre (Premium tech & design roles in India).
    Targets the public job listings by parsing the HTML.
    """
    
    def __init__(self):
        self.base_url = "https://www.instahyre.com/search-jobs"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        self.categories = ["design"]
        
    def scrape(self) -> List[Dict[str, Any]]:
        jobs: List[Dict[str, Any]] = []
        
        with httpx.Client(timeout=20.0, headers=self.headers, follow_redirects=True) as client:
            for category in self.categories:
                try:
                    params = {"skills": category}
                    response = client.get(self.base_url, params=params)
                    
                    if response.status_code != 200:
                        continue
                        
                    soup = BeautifulSoup(response.text, "html.parser")
                    job_cards = soup.find_all("div", class_="employer-block")
                    
                    for card in job_cards:
                        title_el = card.find("div", class_="employer-job-name")
                        company_el = card.find("div", class_="employer-company-name")
                        loc_el = card.find("span", class_="employer-locations")
                        link_el = card.find("a", id="employer-profile-opportunity")
                        exp_el = card.find("span", class_="employer-experience")
                        
                        if not title_el or not company_el:
                            continue
                            
                        job = {
                            "raw_title": title_el.get_text(strip=True),
                            "company_name": company_el.get_text(strip=True),
                            "job_description": "Premium role posted on Instahyre.", # Detail requires clicking
                            "job_location": loc_el.get_text(strip=True) if loc_el else "",
                            "salary": "",
                            "url": "https://www.instahyre.com" + link_el["href"] if link_el else self.base_url,
                            "site": "Instahyre",
                            "date_posted": ""
                        }
                        
                        if exp_el:
                            job["job_description"] += f"\nExperience required: {exp_el.get_text(strip=True)}"
                            
                        jobs.append(job)
                        
                except Exception as e:
                    print(f"[InstahyreScraper] Error fetching '{category}': {e}")
                    continue
                    
        design_jobs = [j for j in jobs if is_design_related(j)]
        return dedupe_jobs(design_jobs)

    def normalize(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        return normalize_job(raw_data, "Instahyre")

