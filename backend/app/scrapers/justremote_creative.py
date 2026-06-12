from typing import Any, Dict, List
from bs4 import BeautifulSoup
from app.scrapers.base import BaseScraper
from app.scrapers.common import ResilientScraperMixin, dedupe_jobs, is_design_related, normalize_job


class JustRemoteScraper(ResilientScraperMixin, BaseScraper):
    """
    Scraper for JustRemote.co — remote-only jobs including a design category.
    Uses their public API.
    """
    API_URL = "https://justremote.co/api/jobs?category=design"

    def __init__(self):
        self.session = self.build_session()

    def scrape(self) -> List[Dict[str, Any]]:
        try:
            data = self.get_json(self.API_URL)
            jobs_raw = data if isinstance(data, list) else data.get("jobs", data.get("data", []))
            jobs = [self._coerce(j) for j in jobs_raw if j]
            jobs = [j for j in jobs if j and is_design_related(j)]
            return dedupe_jobs(jobs)
        except Exception as e:
            print(f"[JustRemoteScraper] Error: {e}")
            return []

    def _coerce(self, item: dict) -> Dict[str, Any]:
        return {
            "raw_title": item.get("title") or item.get("name"),
            "company_name": item.get("company") or item.get("company_name"),
            "job_description": item.get("description") or item.get("excerpt") or "",
            "job_location": item.get("location") or "Remote",
            "salary": item.get("salary"),
            "tags": "remote design justremote",
            "url": item.get("url") or item.get("link") or item.get("apply_url"),
        }

    def normalize(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        return normalize_job(raw_data, "JustRemote")


class CreativepoolScraper(ResilientScraperMixin, BaseScraper):
    """
    Scraper for Creativepool — UK's top creative industry job board.
    """
    JOBS_URL = "https://creativepool.com/jobs"
    CATEGORIES = ["ux-design", "graphic-design", "web-design", "motion-graphics", "art-direction", "brand-design"]

    def __init__(self):
        self.base_url = "https://creativepool.com"
        self.session = self.build_session()

    def scrape(self) -> List[Dict[str, Any]]:
        all_jobs = []
        # Main jobs page
        try:
            html = self.get_html(self.JOBS_URL)
            all_jobs.extend(self._parse(html))
        except Exception as e:
            print(f"[CreativepoolScraper] Main page error: {e}")

        # Category pages
        for cat in self.CATEGORIES:
            try:
                url = f"{self.JOBS_URL}/{cat}"
                html = self.get_html(url)
                all_jobs.extend(self._parse(html))
            except Exception as e:
                print(f"[CreativepoolScraper] Error for '{cat}': {e}")
                continue

        return dedupe_jobs([j for j in all_jobs if is_design_related(j)])

    def _parse(self, html: str) -> List[Dict[str, Any]]:
        soup = BeautifulSoup(html, "html.parser")
        jobs = []
        cards = soup.select(".job-card, .job-listing, article.job, .listing-item")
        for card in cards:
            try:
                title_el = card.select_one("h2, h3, .title, [class*='title']")
                company_el = card.select_one(".company, [class*='company']")
                location_el = card.select_one(".location, [class*='location']")
                link_el = card.select_one("a[href]")
                title = title_el.get_text(strip=True) if title_el else None
                if not title:
                    continue
                href = link_el["href"] if link_el else ""
                url = href if href.startswith("http") else f"{self.base_url}{href}"
                jobs.append({
                    "raw_title": title,
                    "company_name": company_el.get_text(strip=True) if company_el else None,
                    "job_description": f"{title} — creative design role via Creativepool",
                    "job_location": location_el.get_text(strip=True) if location_el else "United Kingdom",
                    "tags": "design creative creativepool uk agency",
                    "url": url,
                })
            except Exception:
                continue
        return jobs

    def normalize(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        return normalize_job(raw_data, "Creativepool")


class SmashingMagScraper(ResilientScraperMixin, BaseScraper):
    """
    Scraper for Smashing Magazine Jobs — highly respected design/dev job board.
    """
    JOBS_URL = "https://jobs.smashingmagazine.com/jobs/design"

    def __init__(self):
        self.base_url = "https://jobs.smashingmagazine.com"
        self.session = self.build_session()

    def scrape(self) -> List[Dict[str, Any]]:
        try:
            html = self.get_html(self.JOBS_URL)
            return dedupe_jobs([j for j in self._parse(html) if is_design_related(j)])
        except Exception as e:
            print(f"[SmashingMagScraper] Error: {e}")
            return []

    def _parse(self, html: str) -> List[Dict[str, Any]]:
        soup = BeautifulSoup(html, "html.parser")
        jobs = []
        cards = soup.select(".job, article, .listing, li.job-listing")
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
                url = href if href.startswith("http") else f"{self.base_url}{href}"
                jobs.append({
                    "raw_title": title,
                    "company_name": company_el.get_text(strip=True) if company_el else None,
                    "job_description": f"{title} — listed on Smashing Magazine Jobs",
                    "job_location": location_el.get_text(strip=True) if location_el else "Remote / Worldwide",
                    "tags": "design smashing magazine ux web",
                    "url": url,
                })
            except Exception:
                continue
        return jobs

    def normalize(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        return normalize_job(raw_data, "Smashing Magazine")

