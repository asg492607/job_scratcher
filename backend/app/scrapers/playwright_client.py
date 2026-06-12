import time
import random
from typing import Optional
from playwright.sync_api import sync_playwright, Browser, Page

class PlaywrightStealthClient:
    """
    Spins up an invisible Chromium browser to bypass JS challenges and Cloudflare.
    Applies stealth techniques to evade automated browser detection.
    """
    
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    ]

    def __init__(self):
        self.playwright = None
        self.browser: Optional[Browser] = None

    def start(self):
        self.playwright = sync_playwright().start()
        try:
            self.browser = self.playwright.chromium.launch(
                headless=True,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--disable-infobars",
                    "--no-sandbox",
                    "--disable-setuid-sandbox"
                ]
            )
        except Exception as e:
            print(f"[PlaywrightStealth] Failed to launch Chromium: {e}")
            self.browser = None

    def stop(self):
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

    def get_html(self, url: str, wait_selector: Optional[str] = None) -> str:
        if not self.browser:
            print("[PlaywrightStealth] Browser not initialized. Returning empty HTML.")
            return ""

        context = self.browser.new_context(
            user_agent=random.choice(self.USER_AGENTS),
            viewport={"width": 1920, "height": 1080},
            java_script_enabled=True,
            bypass_csp=True
        )

        # Stealth Scripts: Delete webdriver property
        context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            window.navigator.chrome = {
                runtime: {},
            };
        """)

        page = context.new_page()
        try:
            # Emulate human delay
            time.sleep(random.uniform(0.5, 1.5))
            
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            
            if wait_selector:
                try:
                    page.wait_for_selector(wait_selector, timeout=10000)
                except Exception:
                    print(f"[PlaywrightStealth] Selector {wait_selector} not found on {url}")
            else:
                # Give JS time to execute if no selector provided
                time.sleep(random.uniform(2, 4))
                
            # Scroll to bottom to trigger lazy loading
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(random.uniform(1, 2))
            
            html = page.content()
            return html
            
        except Exception as e:
            print(f"[PlaywrightStealth] Error fetching {url}: {e}")
            return ""
        finally:
            page.close()
            context.close()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

