from typing import Any, Dict, List
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from app.scrapers.base import BaseScraper
from app.scrapers.common import ResilientScraperMixin, dedupe_jobs, is_design_related, normalize_job


class DribbbleScraper(ResilientScraperMixin, BaseScraper):
    """
    Scraper for Dribbble Jobs — the world's leading design community job board.
    Uses the public jobs page with HTML parsing.
    """

    SEARCH_TAGS = ["ui-ux", "product-design", "visual-design", "graphic-design", "motion-design", "brand-design"]

    def __init__(self):
        self.base_url = "https://dribbble.com"
        self.jobs_url = f"{self.base_url}/jobs"
        self.session = self.build_session()
        self.session.headers.update({
            "Accept": "text/html,application/xhtml+xml",
            "Referer": "https://dribbble.com",
        })

    def scrape(self) -> List[Dict[str, Any]]:
        all_jobs: List[Dict[str, Any]] = []
        try:
            html = self.get_html(self.jobs_url)
            all_jobs.extend(self._parse_jobs(html))
        except Exception as e:
            print(f"[DribbbleScraper] Error scraping main page: {e}")

        # Also scrape by tag
        for tag in self.SEARCH_TAGS:
            try:
                url = f"{self.jobs_url}?tags={tag}"
                html = self.get_html(url)
                all_jobs.extend(self._parse_jobs(html))
            except Exception as e:
                print(f"[DribbbleScraper] Error scraping tag '{tag}': {e}")
                continue

        return dedupe_jobs([j for j in all_jobs if is_design_related(j)])

    def _parse_jobs(self, html: str) -> List[Dict[str, Any]]:
        soup = BeautifulSoup(html, "html.parser")
        jobs = []

        # Dribbble job cards
        cards = (
            soup.select(".job-card") or
            soup.select("article.job") or
            soup.select("[data-job-id]") or
            soup.select(".jobs-board li")
        )

        for card in cards:
            try:
                title_el = card.select_one("h2, h3, .job-title, [class*='title']")
                company_el = card.select_one(".company, [class*='company'], .employer")
                location_el = card.select_one(".location, [class*='location'], .job-location")
                link_el = card.select_one("a[href]")

                title = title_el.get_text(strip=True) if title_el else None
                if not title:
                    continue

                company = company_el.get_text(strip=True) if company_el else None
                location = location_el.get_text(strip=True) if location_el else "Remote"
                href = link_el["href"] if link_el else ""
                url = href if href.startswith("http") else f"{self.base_url}{href}"

                jobs.append({
                    "raw_title": title,
                    "company_name": company,
                    "job_description": f"{title} at {company or 'a design company'} — via Dribbble Jobs",
                    "job_location": location,
                    "tags": "design dribbble creative",
                    "url": url,
                })
            except Exception:
                continue

        # Also check JSON-LD structured data
        for script in soup.find_all("script", type="application/ld+json"):
            try:
                import json
                data = json.loads(script.string or "")
                if isinstance(data, list):
                    for item in data:
                        job = self._from_jsonld(item)
                        if job:
                            jobs.append(job)
                elif isinstance(data, dict):
                    job = self._from_jsonld(data)
                    if job:
                        jobs.append(job)
            except Exception:
                continue

        return jobs

    def _from_jsonld(self, data: dict) -> Dict[str, Any] | None:
        if data.get("@type") not in ("JobPosting", "jobPosting"):
            return None
        hiring_org = data.get("hiringOrganization") or {}
        location = data.get("jobLocation") or {}
        address = location.get("address") or {} if isinstance(location, dict) else {}
        loc_str = address.get("addressLocality") or address.get("addressRegion") or "Remote"
        return {
            "raw_title": data.get("title"),
            "company_name": hiring_org.get("name") if isinstance(hiring_org, dict) else None,
            "job_description": data.get("description", ""),
            "job_location": loc_str,
            "tags": "design dribbble",
            "url": data.get("url") or data.get("sameAs") or self.jobs_url,
        }

    def normalize(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        return normalize_job(raw_data, "Dribbble")

