from typing import Any, Dict, List
import time
import random
import urllib.parse
from bs4 import BeautifulSoup
from app.scrapers.base import BaseScraper
from app.scrapers.common import dedupe_jobs, is_design_related, normalize_job
from app.scrapers.client import RobustHttpClient

class GlassdoorScraper(BaseScraper):
    """
    Scraper for Glassdoor.
    Uses RobustHttpClient to try and bypass Cloudflare to fetch design jobs.
    """
    
    def __init__(self):
        self.base_url = "https://www.glassdoor.co.in/Job/india-design-jobs-SRCH_IL.0,5_IN115_KE6,12.htm"
        
    def scrape(self) -> List[Dict[str, Any]]:
        jobs: List[Dict[str, Any]] = []
        
        with RobustHttpClient() as client:
            try:
                response = client.get(self.base_url)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "html.parser")
                    job_cards = soup.find_all("li", class_="react-job-listing")
                    
                    for card in job_cards:
                        title_el = card.find("a", class_="jobLink")
                        company_el = card.find("div", class_="job-search-8ajk4a") or card.find("a", class_="job-search-1omwz04")
                        loc_el = card.find("span", class_="job-search-1bmuu11") or card.find("div", class_="location")
                        salary_el = card.find("span", class_="job-search-12z0d4a")
                        
                        if not title_el:
                            continue
                            
                        job_url = title_el.get("href", "")
                        if job_url and not job_url.startswith("http"):
                            job_url = "https://www.glassdoor.co.in" + job_url
                            
                        job = {
                            "raw_title": title_el.get_text(strip=True),
                            "company_name": company_el.get_text(strip=True) if company_el else "",
                            "job_description": "",
                            "job_location": loc_el.get_text(strip=True) if loc_el else "India",
                            "salary": salary_el.get_text(strip=True) if salary_el else "",
                            "url": job_url or self.base_url,
                            "site": "Glassdoor",
                            "date_posted": ""
                        }
                        jobs.append(job)
                        
            except Exception as e:
                print(f"[GlassdoorScraper] Error fetching from {self.base_url}: {e}")
                    
        design_jobs = [j for j in jobs if is_design_related(j)]
        return dedupe_jobs(design_jobs)

    def normalize(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        return normalize_job(raw_data, "Glassdoor")
