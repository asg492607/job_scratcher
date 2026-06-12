from typing import Any, Dict, List

from bs4 import BeautifulSoup

from app.scrapers.base import BaseScraper
from app.scrapers.common import ResilientScraperMixin, dedupe_jobs, is_design_related, normalize_job


class ArbeitnowScraper(ResilientScraperMixin, BaseScraper):
    def __init__(self):
        self.api_url = "https://www.arbeitnow.com/api/job-board-api"
        self.session = self.build_session()

    def scrape(self) -> List[Dict[str, Any]]:
        data = self.get_json(self.api_url)
        jobs = [self._coerce_job(item) for item in data.get("data", [])]
        jobs = [job for job in jobs if job and is_design_related(job)]
        return dedupe_jobs(jobs)

    def _coerce_job(self, item: Dict[str, Any]) -> Dict[str, Any]:
        description = BeautifulSoup(item.get("description") or "", "html.parser").get_text(" ", strip=True)
        tags = item.get("tags") or []
        return {
            "raw_title": item.get("title"),
            "company_name": item.get("company_name"),
            "job_description": description or item.get("title"),
            "job_location": item.get("location") or ("Remote" if item.get("remote") else None),
            "tags": " ".join(tags) if isinstance(tags, list) else str(tags),
            "url": item.get("url"),
        }

    def normalize(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        return normalize_job(raw_data, "Arbeitnow")

