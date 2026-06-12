from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseScraper(ABC):
    """
    Base class for all opportunity scrapers.
    """
    
    @abstractmethod
    def scrape(self) -> List[Dict[str, Any]]:
        """
        Executes the scraping logic and returns a list of dictionaries 
        containing raw opportunity data.
        """
        pass
    
    @abstractmethod
    def normalize(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalizes raw scraped data into our standard opportunity schema.
        """
        pass

