import os
import time
from datetime import datetime
from typing import Any, Dict, List

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


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
    "design",
)


class ResilientScraperMixin:
    timeout = 20
    polite_delay_seconds = 1

    def build_session(self) -> requests.Session:
        session = requests.Session()
        retry = Retry(
            total=3,
            connect=3,
            read=3,
            backoff_factor=1,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=("GET",),
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        session.headers.update(
            {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/125.0 Safari/537.36"
                ),
                "Accept-Language": "en-US,en;q=0.9",
            }
        )
        return session

    def get_json(self, url: str) -> Any:
        time.sleep(self.polite_delay_seconds)
        response = self.session.get(url, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def get_html(self, url: str) -> str:
        time.sleep(self.polite_delay_seconds)
        response = self.session.get(url, timeout=self.timeout)
        response.raise_for_status()
        return response.text

    def get_rendered_html(self, url: str, wait_until: str = "networkidle") -> str:
        if os.getenv("ENABLE_BROWSER_SCRAPING", "true").lower() != "true":
            return self.get_html(url)

        from playwright.sync_api import sync_playwright

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page(
                user_agent=self.session.headers.get("User-Agent"),
                locale="en-US",
            )
            page.goto(url, wait_until=wait_until, timeout=self.timeout * 1000)
            html = page.content()
            browser.close()
            return html


def is_design_related(raw_data: Dict[str, Any]) -> bool:
    combined_text = " ".join(
        str(raw_data.get(key) or "")
        for key in ("raw_title", "job_description", "tags")
    ).lower()
    return any(keyword in combined_text for keyword in DESIGN_KEYWORDS)


def infer_remote_status(location: Any) -> str:
    location_text = str(location or "").lower()
    if "remote" in location_text or "anywhere" in location_text:
        return "remote"
    if "hybrid" in location_text:
        return "hybrid"
    return "onsite"


def dedupe_jobs(jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen = set()
    unique_jobs = []
    for job in jobs:
        key = job.get("url") or f"{job.get('raw_title')}:{job.get('company_name')}"
        if key in seen:
            continue
        seen.add(key)
        unique_jobs.append(job)
    return unique_jobs


def normalize_job(raw_data: Dict[str, Any], source: str) -> Dict[str, Any]:
    return {
        "title": raw_data.get("raw_title"),
        "company": raw_data.get("company_name"),
        "description": raw_data.get("job_description"),
        "location": raw_data.get("job_location"),
        "remote_status": infer_remote_status(raw_data.get("job_location")),
        "salary": raw_data.get("salary"),
        "source": source,
        "apply_url": raw_data.get("url"),
        "is_active": True,
        "created_at": datetime.utcnow(),
    }

