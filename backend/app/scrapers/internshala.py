from typing import Any, Dict, List
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from app.scrapers.base import BaseScraper
from app.scrapers.common import ResilientScraperMixin, dedupe_jobs, is_design_related, normalize_job


class IntershalaScraper(ResilientScraperMixin, BaseScraper):
    """
    Scraper for Internshala — India's largest internship platform.
    Targets design internships directly.
    """

    DESIGN_CATEGORIES = [
        "graphic-design",
        "ui-ux",
        "web-design",
        "content-design",
        "animation",
        "illustration",
        "logo-design",
        "photography",
        "video-editing",
    ]

    def __init__(self):
        self.base_url = "https://internshala.com"
        self.session = self.build_session()
        self.session.headers.update({
            "Accept": "application/json, text/html",
            "Referer": "https://internshala.com",
        })

    def scrape(self) -> List[Dict[str, Any]]:
        all_jobs: List[Dict[str, Any]] = []
        for category in self.DESIGN_CATEGORIES:
            try:
                url = f"{self.base_url}/internships/{category}-internship"
                html = self.get_html(url)
                jobs = self._parse_listings(html, category)
                all_jobs.extend(jobs)
            except Exception as e:
                print(f"[IntershalaScraper] Error for category '{category}': {e}")
                continue
        return dedupe_jobs([j for j in all_jobs if is_design_related(j)])

    def _parse_listings(self, html: str, category: str) -> List[Dict[str, Any]]:
        soup = BeautifulSoup(html, "html.parser")
        jobs = []

        # Internshala individual internship containers
        cards = soup.select(".individual_internship") or soup.select(".internship-listing-card")
        for card in cards:
            try:
                title_el = card.select_one(".profile") or card.select_one("h3")
                company_el = card.select_one(".company_name") or card.select_one(".company-name")
                location_el = card.select_one(".location_link") or card.select_one(".locations")
                stipend_el = card.select_one(".stipend") or card.select_one(".stipend_amount")
                link_el = card.select_one("a[href]")

                title = title_el.get_text(strip=True) if title_el else category.replace("-", " ").title()
                company = company_el.get_text(strip=True) if company_el else None
                location = location_el.get_text(strip=True) if location_el else "India"
                stipend = stipend_el.get_text(strip=True) if stipend_el else None
                href = link_el["href"] if link_el else f"/internships/{category}-internship"
                url = href if href.startswith("http") else f"{self.base_url}{href}"

                jobs.append({
                    "raw_title": title,
                    "company_name": company,
                    "job_description": f"{title} internship at {company or 'a company'} — {category.replace('-', ' ')} role",
                    "job_location": location if location else "India",
                    "salary": stipend,
                    "tags": f"internship design {category.replace('-', ' ')} india",
                    "url": url,
                })
            except Exception:
                continue

        return jobs

    def normalize(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        normalized = normalize_job(raw_data, "Internshala")
        normalized["stipend"] = raw_data.get("salary")
        normalized["salary"] = None
        return normalized

