from typing import Any, Dict, List, Optional
from app.scrapers.base import BaseScraper
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from app.scrapers.common import ResilientScraperMixin, dedupe_jobs, is_design_related, normalize_job


class BehanceScraper(ResilientScraperMixin, BaseScraper):
    """
    Scraper for Behance jobs board.
    """
    
    def __init__(self):
        self.base_url = "https://www.behance.net"
        self.joblist_url = f"{self.base_url}/joblist"
        self.session = self.build_session()

    def scrape(self) -> List[Dict[str, Any]]:
        soup = BeautifulSoup(self.get_html(self.joblist_url), "html.parser")
        jobs = self._parse_json_state(soup)
        if not jobs:
            jobs = self._parse_html_cards(soup)
        if not jobs:
            try:
                rendered_soup = BeautifulSoup(self.get_rendered_html(self.joblist_url), "html.parser")
                jobs = self._parse_json_state(rendered_soup) or self._parse_html_cards(rendered_soup)
            except Exception:
                jobs = []

        return [job for job in jobs if is_design_related(job)]

    def _parse_json_state(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        jobs: List[Dict[str, Any]] = []
        for script in soup.find_all("script"):
            script_text = script.string or script.get_text()
            if not script_text or "job" not in script_text.lower():
                continue
            jobs.extend(self._extract_job_objects(script_text))
        return dedupe_jobs(jobs)

    def _extract_job_objects(self, text: str) -> List[Dict[str, Any]]:
        import json
        import re

        jobs: List[Dict[str, Any]] = []
        decoded_objects = self._decode_script_json(text)
        for decoded_object in decoded_objects:
            jobs.extend(self._walk_json_for_jobs(decoded_object))

        for match in re.finditer(r"\{[^{}]*(?:title|jobTitle|name)[^{}]*(?:company|companyName)[^{}]*\}", text):
            try:
                data = json.loads(match.group(0))
            except json.JSONDecodeError:
                continue
            job = self._coerce_job(data)
            if job:
                jobs.append(job)
        return jobs

    def _decode_script_json(self, text: str) -> List[Any]:
        import json
        import re

        decoded = []
        stripped = text.strip()
        candidates = [stripped]

        for pattern in (
            r"window\.__INITIAL_STATE__\s*=\s*(\{.*?\});",
            r"window\.__NEXT_DATA__\s*=\s*(\{.*?\});",
            r"self\.__next_f\.push\(\[.*?,\s*'(.*?)'\]\)",
        ):
            candidates.extend(match.group(1) for match in re.finditer(pattern, text, re.DOTALL))

        for candidate in candidates:
            try:
                decoded.append(json.loads(candidate))
            except json.JSONDecodeError:
                continue
        return decoded

    def _walk_json_for_jobs(self, data: Any) -> List[Dict[str, Any]]:
        jobs: List[Dict[str, Any]] = []
        if isinstance(data, dict):
            coerced = self._coerce_job(data)
            if coerced:
                jobs.append(coerced)
            for value in data.values():
                jobs.extend(self._walk_json_for_jobs(value))
        elif isinstance(data, list):
            for item in data:
                jobs.extend(self._walk_json_for_jobs(item))
        return jobs

    def _parse_html_cards(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        jobs: List[Dict[str, Any]] = []
        for link in soup.find_all("a", href=True):
            href = str(link["href"])
            text = " ".join(link.get_text(" ", strip=True).split())
            if not text or "/joblist/" not in href:
                continue
            title = text.split(" at ")[0].strip()
            if len(title) < 4:
                continue
            jobs.append(
                {
                    "raw_title": title,
                    "company_name": None,
                    "job_description": text,
                    "job_location": None,
                    "url": urljoin(self.base_url, href),
                }
            )
        return dedupe_jobs(jobs)

    def _coerce_job(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        title = data.get("title") or data.get("jobTitle") or data.get("name")
        company = data.get("company") or data.get("companyName") or data.get("company_name")
        description = data.get("description") or data.get("jobDescription") or data.get("summary")
        location = data.get("location") or data.get("jobLocation")
        url = data.get("url") or data.get("applyUrl") or data.get("jobUrl")

        if not title:
            return None

        return {
            "raw_title": title,
            "company_name": company,
            "job_description": description or title,
            "job_location": location,
            "url": urljoin(self.base_url, str(url)) if url else self.joblist_url,
        }

    def normalize(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        return normalize_job(raw_data, "Behance")

