from typing import Any, Dict

from sqlalchemy.orm import Session

from app.categorization.classifier import OpportunityClassifier
from app.repositories.opportunity_repo import OpportunityRepository
from app.schemas.opportunity import OpportunityCreate
from app.scrapers.arbeitnow import ArbeitnowScraper
from app.scrapers.behance import BehanceScraper
from app.scrapers.jobspy_scraper import JobSpyScraper
from app.scrapers.remotive import RemotiveScraper
from app.scrapers.the_muse import TheMuseScraper


class ScrapingService:
    def __init__(self, db: Session):
        self.repo = OpportunityRepository(db)
        self.classifier = OpportunityClassifier()
        self.scrapers = {
            "remotive": RemotiveScraper(),
            "arbeitnow": ArbeitnowScraper(),
            "the_muse": TheMuseScraper(),
            "behance": BehanceScraper(),
            "jobspy": JobSpyScraper(),
        }

    def scrape_source(self, source: str = "behance") -> Dict[str, Any]:
        scraper = self.scrapers.get(source)
        if not scraper:
            return {"source": source, "created": 0, "updated": 0, "error": "Unknown source"}

        try:
            raw_items = scraper.scrape()
        except Exception as error:
            return {
                "source": source,
                "fetched": 0,
                "created": 0,
                "updated": 0,
                "error": str(error),
            }

        created = 0
        updated = 0

        for raw_item in raw_items:
            normalized = scraper.normalize(raw_item)
            classification = self.classifier.classify(
                normalized.get("title") or "",
                normalized.get("description") or "",
            )
            normalized.update(classification)

            opportunity, was_created = self.repo.upsert_by_apply_url(
                OpportunityCreate(**normalized)
            )
            if opportunity and was_created:
                created += 1
            else:
                updated += 1

        return {
            "source": source,
            "fetched": len(raw_items),
            "created": created,
            "updated": updated,
        }

    def scrape_all(self) -> Dict[str, Any]:
        results = [self.scrape_source(source) for source in self.scrapers]
        return {
            "results": results,
            "created": sum(result.get("created", 0) for result in results),
            "updated": sum(result.get("updated", 0) for result in results),
        }
