"""
Browser automation module using Playwright.

Handles all web interactions: platform navigation, form filling,
content scraping, and account creation.
"""

import asyncio
import time
from typing import Optional
from urllib.parse import urlparse

from rich.console import Console

console = Console()


class BrowserAgent:
    """Browser automation agent using Playwright."""

    def __init__(self, headless: bool = False, user_data_dir: Optional[str] = None):
        self.headless = headless
        self.user_data_dir = user_data_dir
        self._browser = None
        self._context = None
        self._page = None
        self._playwright = None

    async def start(self) -> None:
        """Start the browser."""
        try:
            from playwright.async_api import async_playwright
            self._playwright = await async_playwright().start()

            if self.user_data_dir:
                self._context = await self._playwright.chromium.launch_persistent_context(
                    user_data_dir=self.user_data_dir,
                    headless=self.headless,
                    args=[
                        "--disable-blink-features=AutomationControlled",
                        "--no-sandbox",
                    ],
                )
                self._page = self._context.pages[0] if self._context.pages else await self._context.new_page()
            else:
                self._browser = await self._playwright.chromium.launch(
                    headless=self.headless,
                    args=[
                        "--disable-blink-features=AutomationControlled",
                        "--no-sandbox",
                    ],
                )
                self._context = await self._browser.new_context(
                    user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                               "AppleWebKit/537.36 (KHTML, like Gecko) "
                               "Chrome/120.0.0.0 Safari/537.36"
                )
                self._page = await self._context.new_page()

            console.print("[green]✓ Browser started[/]")
        except ImportError:
            console.print("[red]✗ Playwright not installed. Run: pip install playwright && playwright install chromium[/]")
            raise
        except Exception as e:
            console.print(f"[red]✗ Failed to start browser: {e}[/]")
            raise

    async def navigate(self, url: str, wait_until: str = "networkidle") -> bool:
        """Navigate to a URL."""
        try:
            console.print(f"[cyan]🌐 Navigating to: {url}[/]")
            await self._page.goto(url, wait_until=wait_until, timeout=30000)
            return True
        except Exception as e:
            console.print(f"[red]✗ Navigation failed: {e}[/]")
            return False

    async def fill_field(self, selector: str, value: str) -> bool:
        """Fill a form field."""
        try:
            await self._page.fill(selector, value)
            return True
        except Exception as e:
            console.print(f"[red]✗ Failed to fill {selector}: {e}[/]")
            return False

    async def click(self, selector: str) -> bool:
        """Click an element."""
        try:
            await self._page.click(selector)
            return True
        except Exception as e:
            console.print(f"[red]✗ Failed to click {selector}: {e}[/]")
            return False

    async def get_text(self, selector: str) -> str:
        """Get text content of an element."""
        try:
            element = await self._page.query_selector(selector)
            if element:
                return await element.inner_text()
            return ""
        except Exception:
            return ""

    async def get_page_text(self) -> str:
        """Get all visible text from the page."""
        try:
            return await self._page.inner_text("body")
        except Exception:
            return ""

    async def search_freelance_gigs(self, platform: str, keywords: list[str]) -> list[dict]:
        """Search for freelance gigs on a platform."""
        gigs = []
        base_urls = {
            "fiverr": "https://www.fiverr.com/search/gigs",
            "upwork": "https://www.upwork.com/search/jobs",
        }

        url = base_urls.get(platform)
        if not url:
            console.print(f"[red]Unknown platform: {platform}[/]")
            return gigs

        for keyword in keywords[:3]:  # Search top 3 keywords
            try:
                search_url = f"{url}?query={keyword.replace(' ', '+')}&sort=recommended"
                await self.navigate(search_url)

                # Wait for results
                await asyncio.sleep(3)

                # Try to extract gig listings
                text = await self.get_page_text()

                gigs.append({
                    "keyword": keyword,
                    "platform": platform,
                    "url": search_url,
                    "page_text_preview": text[:500],
                    "found": len(text) > 100,
                })

                console.print(f"  [dim]Searched '{keyword}' on {platform}[/]")

            except Exception as e:
                console.print(f"[red]Error searching {platform}: {e}[/]")

        return gigs

    async def take_screenshot(self, path: str = "screenshot.png") -> Optional[str]:
        """Take a screenshot."""
        try:
            await self._page.screenshot(path=path, full_page=True)
            return path
        except Exception:
            return None

    async def detect_captcha(self) -> bool:
        """Detect if a CAPTCHA is present on the page."""
        captcha_indicators = [
            "recaptcha",
            "h-captcha",
            "cf-turnstile",
            "g-recaptcha",
            "captcha",
            "verify you are human",
            "security check",
        ]

        try:
            html = await self._page.content()
            html_lower = html.lower()
            for indicator in captcha_indicators:
                if indicator in html_lower:
                    console.print(f"[yellow]⚠ CAPTCHA detected: {indicator}[/]")
                    return True
            return False
        except Exception:
            return False

    async def wait_for_user_verification(self, message: str = "Please complete the CAPTCHA in the browser window") -> None:
        """
        Pause and wait for the user to complete a CAPTCHA or verification.
        The browser window stays open for the user to interact with.
        """
        console.print(f"\n[bold yellow]🤖 HUMAN VERIFICATION NEEDED[/]")
        console.print(f"[yellow]{message}[/]")
        console.print("[dim]The browser window is open. Complete the verification, then press Enter here.[/]")
        input("Press Enter after completing verification...")
        console.print("[green]✓ Continuing...[/]\n")

    async def fill_form_and_submit(self, fields: dict[str, str], submit_selector: str) -> bool:
        """Fill a multi-field form and submit."""
        try:
            for selector, value in fields.items():
                await self.fill_field(selector, value)
                await asyncio.sleep(0.5)

            await self.click(submit_selector)
            await asyncio.sleep(2)
            return True
        except Exception as e:
            console.print(f"[red]Form submission failed: {e}[/]")
            return False

    async def close(self) -> None:
        """Close the browser."""
        try:
            if self._page:
                await self._page.close()
            if self._context:
                await self._context.close()
            if self._browser:
                await self._browser.close()
            if self._playwright:
                await self._playwright.stop()
            console.print("[dim]Browser closed[/]")
        except Exception:
            pass


# Synchronous wrapper for ease of use
class BrowserAgentSync:
    """Synchronous wrapper for BrowserAgent."""

    def __init__(self, headless: bool = False):
        self.headless = headless
        self._agent = BrowserAgent(headless=headless)

    def start(self) -> None:
        asyncio.run(self._agent.start())

    def navigate(self, url: str) -> bool:
        return asyncio.run(self._agent.navigate(url))

    def search_freelance_gigs(self, platform: str, keywords: list[str]) -> list[dict]:
        return asyncio.run(self._agent.search_freelance_gigs(platform, keywords))

    def detect_captcha(self) -> bool:
        return asyncio.run(self._agent.detect_captcha())

    def wait_for_user_verification(self, message: str = "") -> None:
        asyncio.run(self._agent.wait_for_user_verification(message))

    def close(self) -> None:
        asyncio.run(self._agent.close())
