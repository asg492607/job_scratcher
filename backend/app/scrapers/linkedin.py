from typing import Any, Dict, List
from bs4 import BeautifulSoup
import time
import random
import urllib.parse
from app.scrapers.base import BaseScraper
from app.scrapers.common import dedupe_jobs, is_design_related, normalize_job
from app.scrapers.playwright_client import PlaywrightStealthClient

class LinkedInScraper(BaseScraper):
    """
    Custom robust LinkedIn Scraper targeting the jobs-guest API.
    Utilizes Playwright Stealth Mode to completely bypass anti-bot mechanisms.
    """

    DESIGN_SEARCH_TERMS = [
        "UI UX Designer",
        "Product Designer",
        "Graphic Designer"
    ]

    LOCATIONS = [
        "India",
        "Bangalore Urban, Karnataka, India",
        "Mumbai Metropolitan Region",
        "Delhi, India",
        "Pune, Maharashtra, India",
        "Hyderabad, Telangana, India"
    ]

    def __init__(self):
        # Base public jobs API endpoint
        self.base_url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"

    def scrape(self) -> List[Dict[str, Any]]:
        all_jobs: List[Dict[str, Any]] = []

        with PlaywrightStealthClient() as client:
            for location in self.LOCATIONS:
                for term in self.DESIGN_SEARCH_TERMS:
                    
                    # Deep Pagination: 0 to 1000 jobs (steps of 25) = 40 pages per keyword
                    for start in range(0, 1000, 25):
                        try:
                            # f_TPR=r2592000 means past 30 days
                            params = {
                                "keywords": term,
                                "location": location,
                                "f_TPR": "r2592000",
                                "start": start
                            }
                            
                            url = self.base_url + "?" + urllib.parse.urlencode(params)
                            
                            html = client.get_html(url)
                            if not html:
                                continue
                                
                            soup = BeautifulSoup(html, "html.parser")
                            job_cards = soup.find_all("li")
                            
                            if not job_cards:
                                break # No more jobs for this search
                                
                            for card in job_cards:
                                title_el = card.find("h3", class_="base-search-card__title")
                                company_el = card.find("h4", class_="base-search-card__subtitle")
                                loc_el = card.find("span", class_="job-search-card__location")
                                link_el = card.find("a", class_="base-card__full-link")
                                date_el = card.find("time", class_="job-search-card__listdate")
                                
                                if not title_el or not link_el:
                                    continue
                                    
                                job_url = link_el.get("href", "").split("?")[0]
                                
                                job = {
                                    "raw_title": title_el.get_text(strip=True),
                                    "company_name": company_el.get_text(strip=True) if company_el else "",
                                    "job_description": "Scraped from LinkedIn Public API.", 
                                    "job_location": loc_el.get_text(strip=True) if loc_el else "",
                                    "salary": "",
                                    "url": job_url,
                                    "site": "LinkedIn",
                                    "date_posted": date_el["datetime"] if date_el and date_el.has_attr("datetime") else ""
                                }
                                all_jobs.append(job)
                                
                            # Randomized human-like delay between pages
                            time.sleep(random.uniform(1.5, 3.5))

                        except Exception as e:
                            print(f"[LinkedInScraper] Error scraping '{term}' in '{location}': {e}")
                            continue

        design_jobs = [j for j in all_jobs if is_design_related(j)]
        return dedupe_jobs(design_jobs)

    def normalize(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        return normalize_job(raw_data, "LinkedIn")

