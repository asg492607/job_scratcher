from typing import Any, Dict, List
import httpx
from bs4 import BeautifulSoup
import time
import random
import urllib.parse
from app.scrapers.base import BaseScraper
from app.scrapers.common import dedupe_jobs, is_design_related, normalize_job

class LinkedInScraper(BaseScraper):
    """
    Custom robust LinkedIn Scraper targeting the jobs-guest API.
    Utilizes evasive maneuvers (user-agent rotation, randomized delays, exponential backoff)
    to minimize 429 Too Many Requests blocks on cloud servers.
    """

    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ]

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

    def _get_headers(self):
        return {
            "User-Agent": random.choice(self.USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Cache-Control": "max-age=0"
        }

    def scrape(self) -> List[Dict[str, Any]]:
        all_jobs: List[Dict[str, Any]] = []

        with httpx.Client(timeout=30.0, follow_redirects=True) as client:
            for location in self.LOCATIONS:
                for term in self.DESIGN_SEARCH_TERMS:
                    
                    # We will only pull the first few pages (0, 25, 50) per term/location 
                    # to avoid hitting hard rate limits quickly.
                    for start in [0, 25, 50]:
                        try:
                            # f_TPR=r2592000 means past 30 days
                            params = {
                                "keywords": term,
                                "location": location,
                                "f_TPR": "r2592000",
                                "start": start
                            }
                            
                            headers = self._get_headers()
                            
                            # Exponential backoff loop
                            max_retries = 3
                            for attempt in range(max_retries):
                                response = client.get(self.base_url, params=params, headers=headers)
                                
                                if response.status_code == 200:
                                    break # Success
                                elif response.status_code == 429:
                                    # Rate limited. Backoff.
                                    sleep_time = (2 ** attempt) + random.uniform(1, 3)
                                    print(f"[LinkedInScraper] 429 Rate Limit. Sleeping {sleep_time:.2f}s...")
                                    time.sleep(sleep_time)
                                else:
                                    break # Other error, break out of retry loop

                            if response.status_code != 200:
                                continue # Skip this pagination if still failing
                                
                            soup = BeautifulSoup(response.text, "html.parser")
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
                                    "job_description": "Scraped from LinkedIn Public API.", # Detail requires another req, omit to save rate limits
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
