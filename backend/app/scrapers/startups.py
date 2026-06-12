import httpx
from typing import Any, Dict, List
from datetime import datetime, timezone
from app.scrapers.base import BaseScraper
from app.scrapers.common import dedupe_jobs, is_design_related, normalize_job

class YCombinatorScraper(BaseScraper):
    """Fetches startup jobs from Y Combinator's HackerNews Jobs API."""
    def scrape(self) -> List[Dict[str, Any]]:
        # The HackerNews API provides job stories (usually "Who is hiring" or startup job postings)
        jobs_url = "https://hacker-news.firebaseio.com/v0/jobstories.json"
        
        try:
            with httpx.Client(timeout=15.0) as client:
                response = client.get(jobs_url)
                response.raise_for_status()
                job_ids = response.json()
                
                if not job_ids:
                    return []

                results = []
                # Fetch details for the latest 30 jobs to avoid long API limits
                for job_id in job_ids[:30]:
                    try:
                        item_url = f"https://hacker-news.firebaseio.com/v0/item/{job_id}.json"
                        item_resp = client.get(item_url)
                        item_resp.raise_for_status()
                        job_data = item_resp.json()
                        
                        if not job_data:
                            continue
                            
                        # HN Jobs format is typically: "Company Name is hiring a Role" or just a title with text
                        title = job_data.get("title", "")
                        
                        raw_job = {
                            "raw_title": title,
                            "company_name": "Y Combinator Startup", # Usually parsed from title, but keeping it general
                            "job_description": job_data.get("text", "") or title,
                            "job_location": "Remote", # Default, many HN jobs are remote
                            "url": job_data.get("url") or f"https://news.ycombinator.com/item?id={job_id}",
                            "site": "Y Combinator",
                            "date_posted": str(datetime.fromtimestamp(job_data.get("time", 0), tz=timezone.utc)),
                            "salary": None
                        }
                        
                        if is_design_related(raw_job):
                            results.append(raw_job)
                            
                    except Exception as item_err:
                        print(f"[YCombinatorScraper] Error fetching item {job_id}: {item_err}")
                        continue
                        
                return dedupe_jobs(results)
        except Exception as e:
            print(f"[YCombinatorScraper] Error: {e}")
            return []

    def normalize(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        return normalize_job(raw_data, "Y Combinator")

