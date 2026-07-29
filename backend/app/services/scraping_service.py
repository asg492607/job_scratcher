from typing import Any, Dict

from sqlalchemy.orm import Session

from app.categorization.classifier import OpportunityClassifier
from app.intelligence.pipeline import IntelligencePipeline
from app.repositories.opportunity_repo import OpportunityRepository
from app.schemas.opportunity import OpportunityCreate
from app.scrapers.internshala import IntershalaScraper
from app.scrapers.naukri import NaukriScraper
from app.scrapers.linkedin import LinkedInScraper

from app.repositories.opt_out_repo import OptOutRepository

class ScrapingService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = OpportunityRepository(db)
        self.opt_out_repo = OptOutRepository(db)
        self.classifier = OpportunityClassifier()
        self.pipeline = IntelligencePipeline()
        self.scrapers = {
            "linkedin": LinkedInScraper(),
            "naukri": NaukriScraper(),
            "internshala": IntershalaScraper(),
        }

    def scrape_source(self, source: str = "linkedin") -> Dict[str, Any]:
        """Legacy synchronous scrape method for a single source."""
        scraper = self.scrapers.get(source)
        if not scraper:
            return {"source": source, "created": 0, "updated": 0, "error": "Unknown source"}

        try:
            raw_items = scraper.scrape()
        except Exception as error:
            return {"source": source, "fetched": 0, "created": 0, "updated": 0, "error": str(error)}

        created = 0
        updated = 0

        for raw_item in raw_items:
            try:
                normalized = scraper.normalize(raw_item)
                
                # Check opt-out blocklist under DPDP compliance policy
                if self.opt_out_repo.is_company_blocked(normalized.get("company")):
                    print(f"[ScrapingService] Skipping opted-out company: {normalized.get('company')}")
                    continue

                enhanced_job = self.pipeline.process_job(normalized)
                skills = self.classifier.classify_skills(enhanced_job.get("description", ""))
                enhanced_job["skills"] = list(skills)
                
                opp_data = OpportunityCreate(**enhanced_job)
                opportunity, was_created = self.repo.upsert_by_advanced_dedupe(opp_data)
                
                if opportunity and was_created:
                    created += 1
                else:
                    updated += 1
            except Exception as e:
                print(f"[ScrapingService] Failed to save item from {source}: {e}")
                continue

        return {"source": source, "fetched": len(raw_items), "created": created, "updated": updated}

    def scrape_all(self) -> Dict[str, Any]:
        import concurrent.futures
        
        # 1. Fetch raw items concurrently (Network IO Bound)
        def fetch_raw(source_name: str):
            scraper = self.scrapers.get(source_name)
            try:
                raw_items = scraper.scrape()
                return source_name, raw_items, None
            except Exception as e:
                return source_name, [], str(e)

        results = []
        # Use 3 threads to fetch from all 3 platforms simultaneously
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            future_to_source = {executor.submit(fetch_raw, src): src for src in self.scrapers}
            for future in concurrent.futures.as_completed(future_to_source):
                source_name, raw_items, error = future.result()
                
                if error:
                    results.append({"source": source_name, "fetched": 0, "created": 0, "updated": 0, "error": error})
                    continue
                    
                scraper = self.scrapers[source_name]
                created = 0
                updated = 0
                
                # 2. Process and insert sequentially to protect SQLite from Database Locked errors
                for raw_item in raw_items:
                    try:
                        normalized = scraper.normalize(raw_item)

                        # Check opt-out blocklist under DPDP compliance policy
                        if self.opt_out_repo.is_company_blocked(normalized.get("company")):
                            print(f"[ScrapingService] Skipping opted-out company: {normalized.get('company')}")
                            continue

                        enhanced_job = self.pipeline.process_job(normalized)
                        skills = self.classifier.classify_skills(enhanced_job.get("description", ""))
                        enhanced_job["skills"] = list(skills)
                        
                        opp_data = OpportunityCreate(**enhanced_job)
                        opportunity, was_created = self.repo.upsert_by_advanced_dedupe(opp_data)
                        
                        if opportunity and was_created:
                            created += 1
                        else:
                            updated += 1
                    except Exception as e:
                        print(f"[ScrapingService] Failed to save item from {source_name}: {e}")
                        continue
                        
                results.append({
                    "source": source_name,
                    "fetched": len(raw_items),
                    "created": created,
                    "updated": updated
                })
                
        return {
            "results": results,
            "total_sources": len(results),
            "created": sum(r.get("created", 0) for r in results),
            "updated": sum(r.get("updated", 0) for r in results),
        }


