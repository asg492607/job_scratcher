from typing import Any, Dict, List
import time
import random
from bs4 import BeautifulSoup
from app.scrapers.base import BaseScraper
from app.scrapers.common import dedupe_jobs, is_design_related, normalize_job
from app.scrapers.client import RobustHttpClient

class FounditScraper(BaseScraper):
    """
    Scraper for Foundit (formerly Monster India).
    Targets massive enterprise design jobs in India.
    """
    
    def __init__(self):
        self.base_url = "https://www.foundit.in/srp/results"
        self.keywords = ["ui ux designer", "product designer", "graphic designer", "visual designer"]
        
    def scrape(self) -> List[Dict[str, Any]]:
        jobs: List[Dict[str, Any]] = []
        
        with RobustHttpClient() as client:
            for keyword in self.keywords:
                # Deep pagination: 15 pages deep
                for start_index in range(0, 15 * 50, 50):
                    try:
                        params = {
                            "query": keyword,
                            "searchId": "dummy",
                            "sort": "1", # Sort by newest
                            "limit": 50, # Max per page
                            "start": start_index
                        }
                        
                        response = client.get(self.base_url, params=params)
                        
                        if response.status_code != 200:
                            continue
                            
                        soup = BeautifulSoup(response.text, "html.parser")
                        job_cards = soup.find_all("div", class_="card-apply-content")
                        
                        if not job_cards:
                            job_cards = soup.find_all("div", class_="job-tittle")
                            
                        if not job_cards:
                            break # No more jobs
                            
                        for card in job_cards:
                            title_el = card.find("h3") or card.find("a")
                            company_el = card.find("span", class_="company-name")
                            loc_el = card.find("div", class_="loc") or card.find("span", class_="loc")
                            exp_el = card.find("div", class_="exp") or card.find("span", class_="exp")
                            
                            if not title_el:
                                continue
                                
                            # Try to get link
                            link = ""
                            if title_el.name == "a":
                                link = title_el.get("href", "")
                            else:
                                a_tag = title_el.find("a")
                                if a_tag:
                                    link = a_tag.get("href", "")
                                    
                            if link and not link.startswith("http"):
                                link = "https://www.foundit.in" + link
                                
                            job = {
                                "raw_title": title_el.get_text(strip=True),
                                "company_name": company_el.get_text(strip=True) if company_el else "",
                                "job_description": f"Experience: {exp_el.get_text(strip=True)}" if exp_el else "",
                                "job_location": loc_el.get_text(strip=True) if loc_el else "India",
                                "salary": "",
                                "url": link or self.base_url,
                                "site": "Foundit",
                                "date_posted": ""
                            }
                            jobs.append(job)
                            
                        # Ghost delay
                        time.sleep(random.uniform(1.5, 3.5))
                        
                    except Exception as e:
                        print(f"[FounditScraper] Error fetching '{keyword}' offset {start_index}: {e}")
                        break
                        
        design_jobs = [j for j in jobs if is_design_related(j)]
        return dedupe_jobs(design_jobs)

    def normalize(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        return normalize_job(raw_data, "Foundit")

