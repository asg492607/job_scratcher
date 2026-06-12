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
            # Deep pagination up to 15 pages
            for page in range(1, 16):
                try:
                    # Hirist usually uses ?page=x or similar for pagination. 
                    # If the URL structure changes, this ensures we at least hit multiple endpoints.
                    url = f"{self.base_url}?page={page}" if page > 1 else self.base_url
                    response = client.get(url)
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, "html.parser")
                        job_cards = soup.find_all("div", class_="job-item")
                        
                        if not job_cards:
                            break # No more jobs
                            
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
                            
                        # Ghost delay
                        time.sleep(random.uniform(1.5, 3.5))
                            
                except Exception as e:
                    print(f"[HiristScraper] Error fetching from {self.base_url} page {page}: {e}")
                    break
                    
        design_jobs = [j for j in jobs if is_design_related(j)]
        return dedupe_jobs(design_jobs)

    def normalize(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        return normalize_job(raw_data, "Hirist")

