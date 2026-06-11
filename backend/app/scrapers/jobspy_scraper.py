from typing import Any, Dict, List
from app.scrapers.base import BaseScraper
from app.scrapers.common import dedupe_jobs, is_design_related, normalize_job


class JobSpyScraper(BaseScraper):
    """
    Scraper powered by python-jobspy.
    Aggregates design jobs from LinkedIn, Indeed, Glassdoor, and ZipRecruiter
    in a single call.
    """

    DESIGN_SEARCH_TERMS = [
        "UI UX designer",
        "product designer",
        "graphic designer",
        "visual designer",
        "motion designer",
        "brand designer",
        "design intern",
        "UX researcher",
    ]

    def __init__(
        self,
        site_names: List[str] | None = None,
        locations: List[str] | None = None,
        results_wanted: int = 25,
    ):
        self.site_names = site_names or [
            "indeed",
            "linkedin",
            "glassdoor",
            "zip_recruiter",
        ]
        self.locations = locations or [
            "Remote",
            "United States",
            "United Kingdom",
            "India",
            "Canada",
        ]
        self.results_wanted = results_wanted

    # ── public interface ──────────────────────────────────────────────

    def scrape(self) -> List[Dict[str, Any]]:
        try:
            from jobspy import scrape_jobs
        except ImportError:
            print("[JobSpyScraper] python-jobspy is not installed — skipping.")
            return []

        all_jobs: List[Dict[str, Any]] = []

        for loc in self.locations:
            for term in self.DESIGN_SEARCH_TERMS:
                try:
                    df = scrape_jobs(
                        site_name=self.site_names,
                        search_term=term,
                        location=loc,
                        results_wanted=self.results_wanted,
                        hours_old=72,  # only last 3 days
                    )

                    for _, row in df.iterrows():
                        job = {
                            "raw_title": _str(row.get("title")),
                            "company_name": _str(row.get("company_name")),
                            "job_description": _str(row.get("description")),
                            "job_location": _str(row.get("location")),
                            "salary": _build_salary(row),
                            "url": _str(row.get("job_url")),
                            "site": _str(row.get("site")),
                            "date_posted": _str(row.get("date_posted")),
                        }
                        all_jobs.append(job)

                except Exception as exc:
                    print(f"[JobSpyScraper] Error scraping '{term}' in '{loc}': {exc}")
                    continue

        design_jobs = [j for j in all_jobs if is_design_related(j)]
        return dedupe_jobs(design_jobs)

    def normalize(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        site = raw_data.get("site", "")
        source_label = _SITE_LABELS.get(site.lower(), site.title()) if site else "JobSpy"
        return normalize_job(raw_data, source_label)


# ── helpers ──────────────────────────────────────────────────────────

_SITE_LABELS = {
    "linkedin": "LinkedIn",
    "indeed": "Indeed",
    "glassdoor": "Glassdoor",
    "zip_recruiter": "ZipRecruiter",
}


def _str(value: Any) -> str | None:
    """Convert pandas-like values (including NaN) to str or None."""
    if value is None:
        return None
    import math
    try:
        if isinstance(value, float) and math.isnan(value):
            return None
    except (TypeError, ValueError):
        pass
    text = str(value).strip()
    return text if text else None


def _build_salary(row: Any) -> str | None:
    """Build a salary string from min/max/currency columns if present."""
    lo = row.get("min_amount")
    hi = row.get("max_amount")
    cur = row.get("currency", "")

    parts: List[str] = []
    if lo is not None and _str(lo):
        parts.append(str(lo))
    if hi is not None and _str(hi):
        parts.append(str(hi))
    if not parts:
        return None

    salary = " – ".join(parts)
    if _str(cur):
        salary = f"{cur} {salary}"
    return salary
