from typing import Any, Dict, List
from bs4 import BeautifulSoup
import time
import random
from app.scrapers.base import BaseScraper
from app.scrapers.common import dedupe_jobs, is_design_related, normalize_job
from app.scrapers.client import RobustHttpClient

class NaukriScraper(BaseScraper):
    """
    Scraper for Naukri (India's largest job portal).
    Uses RobustHttpClient for IP rotation to safely paginate 15 pages deep (up to 1500 jobs per keyword).
    """
    
    def __init__(self):
        self.base_url = "https://www.naukri.com/jobapi/v3/search"
        self.headers = {
            "Accept": "application/json",
            "SystemId": "Naukri",
            "AppId": "109",
            "Clientid": "d3sptx"
        }
        self.search_keywords = ["ui ux designer", "product designer", "graphic designer", "visual designer"]
        
    def scrape(self) -> List[Dict[str, Any]]:
        jobs: List[Dict[str, Any]] = []
        
        with RobustHttpClient() as client:
            for keyword in self.search_keywords:
                
                # Deep Pagination: 1 to 15 pages (1500 jobs per keyword)
                for page_num in range(1, 16):
                    try:
                        params = {
                            "noOfResults": 100,
                            "urlType": "search_by_keyword",
                            "searchType": "adv",
                            "keyword": keyword,
                            "pageNo": page_num,
                            "seoKey": keyword.replace(" ", "-") + "-jobs"
                        }
                        
                        response = client.get(self.base_url, params=params, headers=self.headers)
                        if response.status_code != 200:
                            continue
                            
                        data = response.json()
                        raw_jobs = data.get("jobDetails", [])
                        
                        if not raw_jobs:
                            break # No more results for this keyword
                            
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
                            
                        # Ghost delay between pages
                        time.sleep(random.uniform(1.5, 3.5))
                        
                    except Exception as e:
                        print(f"[NaukriScraper] Error fetching '{keyword}' page {page_num}: {e}")
                        break # Skip remaining pages on persistent error
                        
        design_jobs = [j for j in jobs if is_design_related(j)]
        return dedupe_jobs(design_jobs)

    def normalize(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        return normalize_job(raw_data, "Naukri")

