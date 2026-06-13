import httpx
import xml.etree.ElementTree as ET
from typing import Any, Dict, List
from bs4 import BeautifulSoup
from app.scrapers.base import BaseScraper
from app.scrapers.common import dedupe_jobs, is_design_related, normalize_job

class UpworkScraper(BaseScraper):
    """Fetches freelance design jobs from Upwork's RSS feed."""
    def scrape(self) -> List[Dict[str, Any]]:
        # Upwork RSS feed is no longer public (410 Gone)
        return []        
        try:
            with httpx.Client(headers=headers, timeout=15.0) as client:
                response = client.get(rss_url)
                response.raise_for_status()
                
                root = ET.fromstring(response.text)
                results = []
                
                for item in root.findall(".//item"):
                    title = item.findtext("title") or ""
                    description = item.findtext("description") or ""
                    link = item.findtext("link") or ""
                    pub_date = item.findtext("pubDate") or ""
                    
                    raw_job = {
                        "raw_title": title,
                        "company_name": "Upwork Client",
                        "job_description": BeautifulSoup(description, "html.parser").get_text(" ", strip=True),
                        "job_location": "Remote",
                        "url": link,
                        "site": "Upwork",
                        "date_posted": pub_date,
                        "salary": None # Upwork usually embeds budget in description
                    }
                    
                    if is_design_related(raw_job):
                        results.append(raw_job)
                        
                return dedupe_jobs(results)
        except Exception as e:
            print(f"[UpworkScraper] Error: {e}")
            return []

    def normalize(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        return normalize_job(raw_data, "Upwork")


class UXJobsBoardScraper(BaseScraper):
    """Fetches jobs from UXJobsBoard.com."""
    def scrape(self) -> List[Dict[str, Any]]:
        url = "https://www.uxjobsboard.com/"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        
        try:
            with httpx.Client(headers=headers, timeout=15.0) as client:
                response = client.get(url)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, "html.parser")
                jobs = soup.select(".job_listing")
                
                results = []
                for job in jobs:
                    title_elem = job.select_one(".position h3")
                    company_elem = job.select_one(".company strong")
                    location_elem = job.select_one(".location")
                    link_elem = job.select_one("a.job_listing-clickbox")
                    
                    if not title_elem or not link_elem:
                        continue
                        
                    raw_job = {
                        "raw_title": title_elem.get_text(strip=True),
                        "company_name": company_elem.get_text(strip=True) if company_elem else "",
                        "job_description": title_elem.get_text(strip=True), # Details usually on the next page
                        "job_location": location_elem.get_text(strip=True) if location_elem else "Remote",
                        "url": link_elem["href"],
                        "site": "UXJobsBoard",
                        "date_posted": None,
                        "salary": None
                    }
                    
                    results.append(raw_job)
                    
                return dedupe_jobs(results)
        except Exception as e:
            print(f"[UXJobsBoardScraper] Error: {e}")
            return []

    def normalize(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        return normalize_job(raw_data, "UXJobsBoard")

