from typing import Any, Dict, List
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from app.scrapers.base import BaseScraper
from app.scrapers.common import ResilientScraperMixin, dedupe_jobs, is_design_related, normalize_job


class AuthenticJobsScraper(ResilientScraperMixin, BaseScraper):
    """
    Scraper for Authentic Jobs — premium design & creative job board.
    Uses their public RSS feed.
    """

    RSS_URL = "https://authenticjobs.com/feed/"

    def __init__(self):
        self.session = self.build_session()

    def scrape(self) -> List[Dict[str, Any]]:
        try:
            response = self.session.get(self.RSS_URL, timeout=15)
            response.raise_for_status()
            root = ET.fromstring(response.content)
            jobs = []
            for item in root.findall(".//item"):
                job = self._coerce_job(item)
                if job and is_design_related(job):
                    jobs.append(job)
            return dedupe_jobs(jobs)
        except Exception as e:
            print(f"[AuthenticJobsScraper] Error: {e}")
            return []

    def _coerce_job(self, item: ET.Element) -> Dict[str, Any]:
        title = item.findtext("title") or ""
        description_html = item.findtext("description") or ""
        description = BeautifulSoup(description_html, "html.parser").get_text(" ", strip=True)
        
        # Parse location from description or title
        location = "Remote"
        for tag_name in ["{http://purl.org/dc/elements/1.1/}location", "location"]:
            loc = item.findtext(tag_name)
            if loc:
                location = loc
                break

        company = ""
        for tag_name in ["{http://purl.org/dc/elements/1.1/}creator", "creator", "author"]:
            creator = item.findtext(tag_name)
            if creator:
                company = creator
                break

        return {
            "raw_title": title,
            "company_name": company or None,
            "job_description": description or title,
            "job_location": location,
            "tags": "authentic jobs design creative",
            "url": item.findtext("link"),
            "date_posted": item.findtext("pubDate"),
        }

    def normalize(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        return normalize_job(raw_data, "Authentic Jobs")


class CoroflotScraper(ResilientScraperMixin, BaseScraper):
    """
    Scraper for Coroflot — design portfolio & job board used by top agencies.
    """

    JOBS_URL = "https://www.coroflot.com/jobs"

    def __init__(self):
        self.session = self.build_session()

    def scrape(self) -> List[Dict[str, Any]]:
        all_jobs = []
        for page in range(1, 4):  # scrape first 3 pages
            try:
                url = f"{self.JOBS_URL}?page={page}"
                html = self.get_html(url)
                jobs = self._parse_page(html)
                if not jobs:
                    break
                all_jobs.extend(jobs)
            except Exception as e:
                print(f"[CoroflotScraper] Error page {page}: {e}")
                break
        return dedupe_jobs([j for j in all_jobs if is_design_related(j)])

    def _parse_page(self, html: str) -> List[Dict[str, Any]]:
        soup = BeautifulSoup(html, "html.parser")
        jobs = []

        cards = (
            soup.select(".job-listing") or
            soup.select(".jobs-list-item") or
            soup.select("li.job") or
            soup.select("[class*='job-card']")
        )

        for card in cards:
            try:
                title_el = card.select_one("h2, h3, .job-title, [class*='title']")
                company_el = card.select_one(".company, [class*='company']")
                location_el = card.select_one(".location, [class*='location']")
                link_el = card.select_one("a[href]")

                title = title_el.get_text(strip=True) if title_el else None
                if not title:
                    continue

                href = link_el["href"] if link_el else ""
                url = href if href.startswith("http") else f"https://www.coroflot.com{href}"

                jobs.append({
                    "raw_title": title,
                    "company_name": company_el.get_text(strip=True) if company_el else None,
                    "job_description": f"{title} — design role listed on Coroflot",
                    "job_location": location_el.get_text(strip=True) if location_el else "Worldwide",
                    "tags": "design coroflot creative portfolio",
                    "url": url,
                })
            except Exception:
                continue

        return jobs

    def normalize(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        return normalize_job(raw_data, "Coroflot")

