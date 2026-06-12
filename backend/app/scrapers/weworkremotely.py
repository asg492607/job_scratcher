from typing import Any, Dict, List
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

from app.scrapers.base import BaseScraper
from app.scrapers.common import ResilientScraperMixin, dedupe_jobs, is_design_related, normalize_job


class WeWorkRemotelyScraper(ResilientScraperMixin, BaseScraper):
    def __init__(self):
        self.rss_url = "https://weworkremotely.com/categories/remote-design-jobs.rss"
        self.session = self.build_session()

    def scrape(self) -> List[Dict[str, Any]]:
        try:
            response = self.session.get(self.rss_url, timeout=15)
            response.raise_for_status()
            
            root = ET.fromstring(response.content)
            jobs = []
            
            for item in root.findall(".//item"):
                job = self._coerce_job(item)
                if job and is_design_related(job):
                    jobs.append(job)
                    
            return dedupe_jobs(jobs)
        except Exception as e:
            print(f"[WeWorkRemotelyScraper] Error: {e}")
            return []

    def _coerce_job(self, item: ET.Element) -> Dict[str, Any]:
        title = item.findtext("title") or ""
        # WWR titles are often formatted as "Company Name: Job Title"
        company_name = ""
        raw_title = title
        if ":" in title:
            parts = title.split(":", 1)
            company_name = parts[0].strip()
            raw_title = parts[1].strip()

        description_html = item.findtext("description") or ""
        description = BeautifulSoup(description_html, "html.parser").get_text(" ", strip=True)
        
        return {
            "raw_title": raw_title,
            "company_name": company_name,
            "job_description": description,
            "job_location": "Remote",
            "tags": item.findtext("category") or "Design",
            "url": item.findtext("link"),
            "date_posted": item.findtext("pubDate"),
        }

    def normalize(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        return normalize_job(raw_data, "We Work Remotely")

