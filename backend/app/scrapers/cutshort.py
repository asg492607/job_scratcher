from typing import Any, Dict, List
import httpx
from bs4 import BeautifulSoup
from app.scrapers.base import BaseScraper
from app.scrapers.common import dedupe_jobs, is_design_related, normalize_job

class CutShortScraper(BaseScraper):
    """
    Scraper for CutShort (Startup & Tech match-making platform in India).
    Scrapes their public job directory pages.
    """
    
    def __init__(self):
        self.base_url = "https://cutshort.io/jobs"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        }
        self.categories = ["ui-ux-designer-jobs", "product-designer-jobs", "graphic-designer-jobs"]
        
    def scrape(self) -> List[Dict[str, Any]]:
        jobs: List[Dict[str, Any]] = []
        
        with httpx.Client(timeout=15.0, headers=self.headers, follow_redirects=True) as client:
            for category in self.categories:
                try:
                    # e.g., https://cutshort.io/jobs/ui-ux-designer-jobs
                    url = f"{self.base_url}/{category}"
                    response = client.get(url)
                    
                    if response.status_code != 200:
                        continue
                        
                    soup = BeautifulSoup(response.text, "html.parser")
                    job_cards = soup.find_all("div", class_="job-card")
                    
                    for card in job_cards:
                        title_el = card.find("h3")
                        company_el = card.find("div", class_="company-name")
                        loc_el = card.find("div", class_="locations")
                        link_el = card.find("a")
                        
                        if not title_el or not company_el:
                            continue
                            
                        job = {
                            "raw_title": title_el.get_text(strip=True),
                            "company_name": company_el.get_text(strip=True),
                            "job_description": "", # Extracted inside pipeline if URL provided
                            "job_location": loc_el.get_text(strip=True) if loc_el else "",
                            "salary": "",
                            "url": "https://cutshort.io" + link_el["href"] if link_el else url,
                            "site": "CutShort",
                            "date_posted": ""
                        }
                        jobs.append(job)
                        
                except Exception as e:
                    print(f"[CutShortScraper] Error fetching '{category}': {e}")
                    continue
                    
        design_jobs = [j for j in jobs if is_design_related(j)]
        return dedupe_jobs(design_jobs)

    def normalize(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        return normalize_job(raw_data, "CutShort")

