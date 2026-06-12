from typing import Any, Dict, List

from bs4 import BeautifulSoup

from app.scrapers.base import BaseScraper
from app.scrapers.common import ResilientScraperMixin, dedupe_jobs, is_design_related, normalize_job


class TheMuseScraper(ResilientScraperMixin, BaseScraper):
    def __init__(self):
        self.api_url = "https://www.themuse.com/api/public/jobs?category=Design%20and%20UX&page=1"
        self.session = self.build_session()

    def scrape(self) -> List[Dict[str, Any]]:
        data = self.get_json(self.api_url)
        jobs = [self._coerce_job(item) for item in data.get("results", [])]
        jobs = [job for job in jobs if job and is_design_related(job)]
        return dedupe_jobs(jobs)

    def _coerce_job(self, item: Dict[str, Any]) -> Dict[str, Any]:
        company = item.get("company") or {}
        locations = item.get("locations") or []
        refs = item.get("refs") or {}
        contents = BeautifulSoup(item.get("contents") or "", "html.parser").get_text(" ", strip=True)

        return {
            "raw_title": item.get("name"),
            "company_name": company.get("name"),
            "job_description": contents or item.get("name"),
            "job_location": ", ".join(location.get("name", "") for location in locations if location.get("name")),
            "tags": "Design UX",
            "url": refs.get("landing_page"),
        }

    def normalize(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        return normalize_job(raw_data, "The Muse")

