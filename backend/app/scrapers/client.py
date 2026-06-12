import httpx
import time
import random
from typing import Any, Dict, Optional

class RobustHttpClient:
    """
    Enterprise-Grade HttpClient for scraping.
    Automatically rotates User-Agents, injects human-like delays, 
    and performs Exponential Backoff on 429/403 errors.
    """
    
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Mobile/15E148 Safari/604.1"
    ]

    def __init__(self, timeout: float = 30.0, max_retries: int = 3):
        self.timeout = timeout
        self.max_retries = max_retries
        self._client = httpx.Client(timeout=self.timeout, follow_redirects=True)

    def _get_random_headers(self, custom_headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        headers = {
            "User-Agent": random.choice(self.USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1"
        }
        if custom_headers:
            headers.update(custom_headers)
        return headers

    def get(self, url: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> httpx.Response:
        """
        Performs a GET request with automatic retry, backoff, and UA rotation.
        """
        req_headers = self._get_random_headers(headers)
        
        for attempt in range(self.max_retries):
            try:
                response = self._client.get(url, params=params, headers=req_headers)
                
                if response.status_code in [200, 201, 204]:
                    return response
                    
                if response.status_code in [429, 403]:
                    # Rate limited or forbidden block. Exponential backoff.
                    sleep_time = (2 ** attempt) + random.uniform(1, 3)
                    print(f"[RobustHttpClient] {response.status_code} Blocked. Sleeping {sleep_time:.2f}s...")
                    time.sleep(sleep_time)
                    # Rotate UA for the next attempt
                    req_headers["User-Agent"] = random.choice(self.USER_AGENTS)
                    continue
                    
                # If it's a 404 or 500, we just return the response and let the caller handle it.
                return response
                
            except (httpx.RequestError, httpx.TimeoutException) as e:
                print(f"[RobustHttpClient] Network Error: {e}")
                sleep_time = (2 ** attempt) + random.uniform(1, 3)
                time.sleep(sleep_time)
                
        # If we exhausted all retries, return the last response (which may be a 403 or 429)
        return response

    def close(self):
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
