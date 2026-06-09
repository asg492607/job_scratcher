from typing import Any, Dict, List, Optional
from app.scrapers.base import BaseScraper
from datetime import datetime
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


DESIGN_KEYWORDS = (
    "ui",
    "ux",
    "user interface",
    "user experience",
    "product design",
    "graphic design",
    "visual design",
    "brand design",
    "motion design",
    "animation",
    "illustrator",
    "illustration",
    "figma",
    "photoshop",
    "designer",
)

class BehanceScraper(BaseScraper):
    """
    Scraper for Behance jobs board.
    """
    
    def __init__(self):
        self.base_url = "https://www.behance.net"
        self.joblist_url = f"{self.base_url}/joblist"
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/125.0 Safari/537.36"
                ),
                "Accept-Language": "en-US,en;q=0.9",
            }
        )

    def scrape(self) -> List[Dict[str, Any]]:
        response = self.session.get(self.joblist_url, timeout=20)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        jobs = self._parse_json_state(soup)
        if not jobs:
            jobs = self._parse_html_cards(soup)

        return [job for job in jobs if self._is_design_related(job)]

    def _parse_json_state(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        jobs: List[Dict[str, Any]] = []
        for script in soup.find_all("script"):
            script_text = script.string or script.get_text()
            if not script_text or "job" not in script_text.lower():
                continue
            jobs.extend(self._extract_job_objects(script_text))
        return self._dedupe(jobs)

    def _extract_job_objects(self, text: str) -> List[Dict[str, Any]]:
        import json
        import re

        jobs: List[Dict[str, Any]] = []
        for match in re.finditer(r"\{[^{}]*(?:title|jobTitle|name)[^{}]*(?:company|companyName)[^{}]*\}", text):
            try:
                data = json.loads(match.group(0))
            except json.JSONDecodeError:
                continue
            job = self._coerce_job(data)
            if job:
                jobs.append(job)
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
        return self._dedupe(jobs)

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

    def _is_design_related(self, raw_data: Dict[str, Any]) -> bool:
        combined_text = " ".join(
            str(raw_data.get(key) or "")
            for key in ("raw_title", "job_description")
        ).lower()
        return any(keyword in combined_text for keyword in DESIGN_KEYWORDS)

    def _dedupe(self, jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        seen = set()
        unique_jobs = []
        for job in jobs:
            key = job.get("url") or f"{job.get('raw_title')}:{job.get('company_name')}"
            if key in seen:
                continue
            seen.add(key)
            unique_jobs.append(job)
        return unique_jobs
        
    def normalize(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        # Convert the raw Behance dictionary into our system's Opportunity schema format
        return {
            "title": raw_data.get("raw_title"),
            "company": raw_data.get("company_name"),
            "description": raw_data.get("job_description"),
            "location": raw_data.get("job_location"),
            "remote_status": "remote" if "remote" in str(raw_data.get("job_location")).lower() else "onsite",
            "source": "Behance",
            "apply_url": raw_data.get("url"),
            "is_active": True,
            "created_at": datetime.utcnow()
        }
