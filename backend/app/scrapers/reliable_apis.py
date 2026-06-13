import httpx
from typing import Any, Dict, List
from app.scrapers.base import BaseScraper
from app.scrapers.common import dedupe_jobs, is_design_related, normalize_job

class RemoteOKScraper(BaseScraper):
    """Fetches design jobs from RemoteOK public API."""
    def scrape(self) -> List[Dict[str, Any]]:
        # RemoteOK now blocks with 403 Forbidden
        return []
                data = response.json()
                
                # RemoteOK API returns a legal/stats object as the first item in the array
                if data and isinstance(data, list) and len(data) > 0:
                    jobs_data = data[1:]
                else:
                    return []

                results = []
                for job in jobs_data:
                    raw_job = {
                        "raw_title": job.get("position"),
                        "company_name": job.get("company"),
                        "job_description": job.get("description"),
                        "job_location": job.get("location") or "Remote",
                        "url": job.get("url"),
                        "site": "RemoteOK",
                        "date_posted": job.get("date"),
                        "salary": f"{job.get('salary_min', '')} - {job.get('salary_max', '')}".strip(" -")
                    }
                    if is_design_related(raw_job):
                        results.append(raw_job)
                
                return dedupe_jobs(results)
        except Exception as e:
            print(f"[RemoteOKScraper] Error: {e}")
            return []

    def normalize(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        return normalize_job(raw_data, "RemoteOK")


class HimalayasScraper(BaseScraper):
    """Fetches design jobs from Himalayas public API."""
    def scrape(self) -> List[Dict[str, Any]]:
        # Limit 100 per page, offset can be added if needed
        url = "https://himalayas.app/jobs/api?limit=100"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        try:
            with httpx.Client(headers=headers, timeout=15.0) as client:
                response = client.get(url)
                response.raise_for_status()
                data = response.json()
                
                jobs_data = data.get("jobs", [])
                
                results = []
                for job in jobs_data:
                    raw_job = {
                        "raw_title": job.get("title"),
                        "company_name": job.get("companyName"),
                        "job_description": job.get("excerpt") or job.get("description"),
                        "job_location": job.get("locationRestrictions", ["Remote"])[0] if job.get("locationRestrictions") else "Remote",
                        "url": job.get("applicationLink") or job.get("jobUrl"),
                        "site": "Himalayas",
                        "date_posted": str(job.get("pubDate")),
                        "salary": None
                    }
                    if is_design_related(raw_job):
                        results.append(raw_job)
                
                return dedupe_jobs(results)
        except Exception as e:
            print(f"[HimalayasScraper] Error: {e}")
            return []

    def normalize(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        return normalize_job(raw_data, "Himalayas")

