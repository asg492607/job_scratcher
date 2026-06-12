from typing import Any, Dict, List
import time
import random
from bs4 import BeautifulSoup
from app.scrapers.base import BaseScraper
from app.scrapers.common import dedupe_jobs, is_design_related, normalize_job
from app.scrapers.client import RobustHttpClient

class HiristScraper(BaseScraper):
    """
    Scraper for Hirist.
    Targets premium Indian IT and tech startups, specifically their UI/UX job board.
    """
    
    def __init__(self):
        self.base_url = "https://www.hirist.tech/search/ui-ux-jobs.html"
        
    def scrape(self) -> List[Dict[str, Any]]:
        jobs: List[Dict[str, Any]] = []
        
        with RobustHttpClient() as client:
            try:
                response = client.get(self.base_url)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "html.parser")
                    job_cards = soup.find_all("div", class_="job-item")
                    
                    for card in job_cards:
                        title_el = card.find("span", class_="title") or card.find("h3")
                        company_el = card.find("span", class_="company") or card.find("div", class_="company-name")
                        loc_el = card.find("span", class_="location")
                        exp_el = card.find("span", class_="experience")
                        link_el = card.find("a")
                        
                        if not title_el:
                            continue
                            
                        job_url = link_el.get("href", "") if link_el else ""
                        if job_url and not job_url.startswith("http"):
                            job_url = "https://www.hirist.tech" + job_url
                            
                        job = {
                            "raw_title": title_el.get_text(strip=True),
                            "company_name": company_el.get_text(strip=True) if company_el else "",
                            "job_description": f"Experience: {exp_el.get_text(strip=True)}" if exp_el else "",
                            "job_location": loc_el.get_text(strip=True) if loc_el else "India",
                            "salary": "",
                            "url": job_url or self.base_url,
                            "site": "Hirist",
                            "date_posted": ""
                        }
                        jobs.append(job)
                        
            except Exception as e:
                print(f"[HiristScraper] Error fetching from {self.base_url}: {e}")
                    
        design_jobs = [j for j in jobs if is_design_related(j)]
        return dedupe_jobs(design_jobs)

    def normalize(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        return normalize_job(raw_data, "Hirist")
