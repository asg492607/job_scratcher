from typing import Any, Dict, List
from bs4 import BeautifulSoup
import time
import random
from app.scrapers.base import BaseScraper
from app.scrapers.common import dedupe_jobs, is_design_related, normalize_job
from app.scrapers.client import RobustHttpClient
from app.scrapers.playwright_client import PlaywrightStealthClient

class NaukriScraper(BaseScraper):
    """
    Scraper for Naukri (India's largest job portal).
    Tries API extraction via RobustHttpClient and falls back to Playwright Stealth HTML extraction
    to ensure uninterrupted data collection.
    """
    
    def __init__(self):
        self.base_url = "https://www.naukri.com/jobapi/v3/search"
        self.headers = {
            "Accept": "application/json",
            "SystemId": "Naukri",
            "AppId": "109",
            "Clientid": "d3sptx",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }
        self.search_keywords = ["ui ux designer", "product designer", "graphic designer", "visual designer"]
        
    def scrape(self) -> List[Dict[str, Any]]:
        jobs: List[Dict[str, Any]] = []
        
        # 1. Primary Extraction: Try API Search
        with RobustHttpClient() as client:
            for keyword in self.search_keywords:
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
                            break
                            
                        data = response.json()
                        raw_jobs = data.get("jobDetails", [])
                        
                        if not raw_jobs:
                            break
                            
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
                            
                        time.sleep(random.uniform(1.5, 3.5))
                        
                    except Exception as e:
                        print(f"[NaukriScraper] API Error for '{keyword}': {e}")
                        break

        # 2. Fallback Extraction: If API blocked, use Playwright Stealth Client HTML parsing
        if not jobs:
            print("[NaukriScraper] API extraction blocked; initiating Playwright Stealth HTML scraper...")
            with PlaywrightStealthClient() as pw_client:
                for keyword in self.search_keywords[:2]:
                    try:
                        url = f"https://www.naukri.com/{keyword.replace(' ', '-')}-jobs"
                        html = pw_client.get_html(url, wait_selector=".srp-jobtuple-wrapper")
                        if html:
                            soup = BeautifulSoup(html, "html.parser")
                            cards = soup.select(".srp-jobtuple-wrapper") or soup.select("article.jobTuple")
                            for card in cards:
                                title_el = card.select_one(".title") or card.select_one("a.title")
                                company_el = card.select_one(".comp-name") or card.select_one("a.subTitle")
                                loc_el = card.select_one(".loc-wrap") or card.select_one(".location")
                                sal_el = card.select_one(".sal-wrap") or card.select_one(".salary")
                                link_el = title_el if title_el and title_el.name == 'a' else card.select_one("a[href]")

                                if title_el:
                                    href = link_el["href"] if link_el and link_el.has_attr("href") else url
                                    jobs.append({
                                        "raw_title": title_el.get_text(strip=True),
                                        "company_name": company_el.get_text(strip=True) if company_el else "Naukri Listing",
                                        "job_description": f"{title_el.get_text(strip=True)} role at {company_el.get_text(strip=True) if company_el else 'company'}",
                                        "job_location": loc_el.get_text(strip=True) if loc_el else "India",
                                        "salary": sal_el.get_text(strip=True) if sal_el else "",
                                        "url": href if href.startswith("http") else f"https://www.naukri.com{href}",
                                        "site": "Naukri"
                                    })
                    except Exception as e:
                        print(f"[NaukriScraper] Playwright fallback error for '{keyword}': {e}")

        design_jobs = [j for j in jobs if is_design_related(j)]
        return dedupe_jobs(design_jobs)

    def normalize(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        return normalize_job(raw_data, "Naukri")
