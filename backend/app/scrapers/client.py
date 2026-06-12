import httpx
import time
import random
import requests
from typing import Any, Dict, Optional

class ProxyManager:
    """Fetches and manages a pool of free public proxies."""
    _proxies = []
    _last_fetched = 0
    _fetch_interval = 3600 # 1 hour

    @classmethod
    def get_proxy(cls) -> Optional[str]:
        current_time = time.time()
        if not cls._proxies or (current_time - cls._last_fetched > cls._fetch_interval):
            cls._fetch_proxies()
        
        if not cls._proxies:
            return None
            
        return random.choice(cls._proxies)

    @classmethod
    def _fetch_proxies(cls):
        try:
            # Fetch free HTTP/HTTPS proxies from ProxyScrape
            url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                proxy_list = response.text.strip().split("\r\n")
                # Format: "ip:port" -> "http://ip:port"
                cls._proxies = [f"http://{p}" for p in proxy_list if p]
                cls._last_fetched = time.time()
                print(f"[ProxyManager] Successfully fetched {len(cls._proxies)} proxies.")
        except Exception as e:
            print(f"[ProxyManager] Failed to fetch proxies: {e}")

class RobustHttpClient:
    """
    Enterprise-Grade HttpClient for scraping.
    Automatically rotates User-Agents, injects human-like delays, 
    rotates IP Addresses via Free Proxies, and performs Exponential Backoff.
    """
    
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Mobile/15E148 Safari/604.1"
    ]

    def __init__(self, timeout: float = 30.0, max_retries: int = 4):
        self.timeout = timeout
        self.max_retries = max_retries

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
        Performs a GET request with automatic retry, backoff, UA rotation, and IP rotation.
        """
        req_headers = self._get_random_headers(headers)
        last_response = None
        
        for attempt in range(self.max_retries):
            proxy_url = ProxyManager.get_proxy()
            proxies = {"http://": proxy_url, "https://": proxy_url} if proxy_url else None
            
            try:
                # Create a fresh client for each attempt to cleanly handle proxy rotation
                with httpx.Client(timeout=self.timeout, proxies=proxies, follow_redirects=True) as client:
                    response = client.get(url, params=params, headers=req_headers)
                    last_response = response
                    
                    if response.status_code in [200, 201, 204]:
                        return response
                        
                    if response.status_code in [429, 403]:
                        # Rate limited or forbidden block. 
                        sleep_time = (2 ** attempt) + random.uniform(1, 3)
                        print(f"[RobustHttpClient] {response.status_code} Blocked. Rotating Proxy and Sleeping {sleep_time:.2f}s...")
                        time.sleep(sleep_time)
                        
                        # Remove the dead proxy from the pool
                        if proxy_url and proxy_url in ProxyManager._proxies:
                            ProxyManager._proxies.remove(proxy_url)
                            
                        # Rotate UA for the next attempt
                        req_headers["User-Agent"] = random.choice(self.USER_AGENTS)
                        continue
                        
                    # 404 or 500, break out and return
                    return response
                    
            except (httpx.RequestError, httpx.TimeoutException) as e:
                # Network error, usually means the free proxy is dead
                if proxy_url and proxy_url in ProxyManager._proxies:
                    ProxyManager._proxies.remove(proxy_url)
                    
                sleep_time = random.uniform(0.5, 2)
                time.sleep(sleep_time)
                
        # If we exhausted all retries, return the last response (if any) or raise
        if last_response is not None:
            return last_response
        raise Exception(f"[RobustHttpClient] All {self.max_retries} attempts failed due to dead proxies or network errors.")

    def close(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

