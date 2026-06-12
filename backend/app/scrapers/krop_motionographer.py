from typing import Any, Dict, List
from bs4 import BeautifulSoup
from app.scrapers.base import BaseScraper
from app.scrapers.common import ResilientScraperMixin, dedupe_jobs, is_design_related, normalize_job


class KropScraper(ResilientScraperMixin, BaseScraper):
    """
    Scraper for Krop — design & creative job board focused on portfolio professionals.
    """

    CATEGORIES = [
        "ui-ux-design",
        "graphic-design",
        "web-design",
        "art-direction",
        "motion-graphics",
        "product-design",
    ]

    def __init__(self):
        self.base_url = "https://www.krop.com"
        self.session = self.build_session()

    def scrape(self) -> List[Dict[str, Any]]:
        all_jobs = []
        for category in self.CATEGORIES:
            try:
                url = f"{self.base_url}/creativejobs/?discipline={category}"
                html = self.get_html(url)
                jobs = self._parse_page(html, category)
                all_jobs.extend(jobs)
            except Exception as e:
                print(f"[KropScraper] Error for '{category}': {e}")
                continue
        return dedupe_jobs([j for j in all_jobs if is_design_related(j)])

    def _parse_page(self, html: str, category: str) -> List[Dict[str, Any]]:
        soup = BeautifulSoup(html, "html.parser")
        jobs = []

        cards = (
            soup.select(".job-listing") or
            soup.select(".job_listing") or
            soup.select("li.job") or
            soup.select("[class*='listing']") or
            soup.select(".jobs li")
        )

        for card in cards:
            try:
                title_el = card.select_one("h2, h3, .title, [class*='title'], a")
                company_el = card.select_one(".company, [class*='company']")
                location_el = card.select_one(".location, [class*='location'], .city")
                link_el = card.select_one("a[href]")

                title = title_el.get_text(strip=True) if title_el else None
                if not title or len(title) < 3:
                    continue

                href = link_el["href"] if link_el else ""
                url = href if href.startswith("http") else f"{self.base_url}{href}"

                jobs.append({
                    "raw_title": title,
                    "company_name": company_el.get_text(strip=True) if company_el else None,
                    "job_description": f"{title} — {category.replace('-', ' ')} role via Krop",
                    "job_location": location_el.get_text(strip=True) if location_el else "Worldwide",
                    "tags": f"design krop creative {category.replace('-', ' ')}",
                    "url": url,
                })
            except Exception:
                continue

        return jobs

    def normalize(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        return normalize_job(raw_data, "Krop")


class MotionographerScraper(ResilientScraperMixin, BaseScraper):
    """
    Scraper for Motionographer — the definitive source for motion design jobs.
    """

    JOBS_URL = "https://motionographer.com/category/jobs/"

    def __init__(self):
        self.session = self.build_session()

    def scrape(self) -> List[Dict[str, Any]]:
        try:
            html = self.get_html(self.JOBS_URL)
            return dedupe_jobs(self._parse_page(html))
        except Exception as e:
            print(f"[MotionographerScraper] Error: {e}")
            return []

    def _parse_page(self, html: str) -> List[Dict[str, Any]]:
        soup = BeautifulSoup(html, "html.parser")
        jobs = []

        articles = soup.select("article, .post, .job-post")
        for article in articles:
            try:
                title_el = article.select_one("h1, h2, h3, .entry-title, .post-title")
                link_el = article.select_one("a[href]")
                excerpt_el = article.select_one(".excerpt, .entry-summary, p")

                title = title_el.get_text(strip=True) if title_el else None
                if not title:
                    continue

                href = link_el["href"] if link_el else ""
                excerpt = excerpt_el.get_text(strip=True) if excerpt_el else ""

                jobs.append({
                    "raw_title": title,
                    "company_name": None,
                    "job_description": excerpt or f"{title} — motion design job via Motionographer",
                    "job_location": "Remote / Worldwide",
                    "tags": "motion design animation motionographer film",
                    "url": href if href.startswith("http") else f"https://motionographer.com{href}",
                })
            except Exception:
                continue

        return jobs

    def normalize(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        return normalize_job(raw_data, "Motionographer")

