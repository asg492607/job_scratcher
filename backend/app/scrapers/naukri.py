from typing import Any, Dict, List
import httpx
from bs4 import BeautifulSoup
import time
from app.scrapers.base import BaseScraper
from app.scrapers.common import dedupe_jobs, is_design_related, normalize_job

class NaukriScraper(BaseScraper):
    """
    Scraper for Naukri (India's largest job portal).
    Naukri heavily protects its APIs with Cloudflare/Akamai, so we make a best-effort 
    API request to their public search endpoint.
    """
    
    def __init__(self):
        self.base_url = "https://www.naukri.com/jobapi/v3/search"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json",
            "SystemId": "Naukri",
            "AppId": "109",
            "Clientid": "d3sptx"
        }
        self.search_keywords = ["ui ux designer", "product designer", "graphic designer", "visual designer"]
        
    def scrape(self) -> List[Dict[str, Any]]:
        jobs: List[Dict[str, Any]] = []
        
        with httpx.Client(timeout=15.0, headers=self.headers) as client:
            for keyword in self.search_keywords:
                try:
                    params = {
                        "noOfResults": 100,
                        "urlType": "search_by_keyword",
                        "searchType": "adv",
                        "keyword": keyword,
                        "pageNo": 1,
                        "seoKey": keyword.replace(" ", "-") + "-jobs"
                    }
                    
                    response = client.get(self.base_url, params=params)
                    if response.status_code != 200:
                        continue
                        
                    data = response.json()
                    raw_jobs = data.get("jobDetails", [])
                    
                    for raw in raw_jobs:
                        job = {
                            "raw_title": raw.get("title", ""),
                            "company_name": raw.get("companyName", ""),
                            "job_description": BeautifulSoup(raw.get("jobDescription", ""), "html.parser").get_text() if raw.get("jobDescription") else "",
                            "job_location": next(iter(raw.get("placeholders", [])), {}).get("label", ""),
                            "salary": raw.get("salary", ""),
                            "url": raw.get("jdURL", ""),
                            "site": "Naukri",
                            "date_posted": str(raw.get("createdDate", ""))
                        }
                        jobs.append(job)
                        
                    time.sleep(2)  # Respect rate limits
                    
                except Exception as e:
                    print(f"[NaukriScraper] Error fetching '{keyword}': {e}")
                    continue
                    
        design_jobs = [j for j in jobs if is_design_related(j)]
        return dedupe_jobs(design_jobs)

    def normalize(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        return normalize_job(raw_data, "Naukri")
