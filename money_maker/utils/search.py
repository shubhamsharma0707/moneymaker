"""
Web search capabilities using free APIs.

Searches the web for earning opportunities, market research,
and client contact information.
"""

import urllib.parse
import json
import httpx
from typing import Optional

from rich.console import Console

console = Console()


class WebSearch:
    """Web search engine for finding opportunities and information."""

    def __init__(self):
        self._http_client = httpx.Client(timeout=15.0)

    def search(self, query: str, num_results: int = 5) -> list[dict]:
        """
        Search the web using DuckDuckGo (free, no API key needed).

        Falls back to Google scraping if DDG fails.
        """
        results = self._search_duckduckgo(query, num_results)
        if not results:
            results = self._search_google_fallback(query, num_results)
        return results

    def _search_duckduckgo(self, query: str, num_results: int) -> list[dict]:
        """Search using DuckDuckGo Lite API (free)."""
        try:
            url = f"https://lite.duckduckgo.com/lite/?q={urllib.parse.quote(query)}"
            response = self._http_client.get(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                                  "AppleWebKit/537.36"
                },
            )

            if response.status_code == 200:
                # Parse the HTML response
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.text, "html.parser")
                results = []

                # DDG Lite has a simple table structure
                for link in soup.select("a[href^='http']")[:num_results]:
                    text = link.get_text(strip=True)
                    href = link.get("href", "")
                    if text and href:
                        results.append({
                            "title": text,
                            "url": href,
                            "snippet": "",
                        })

                return results
        except Exception as e:
            console.print(f"[dim]DDG search failed: {e}[/]")

        return []

    def _search_google_fallback(self, query: str, num_results: int) -> list[dict]:
        """Fallback: scrape Google search results."""
        try:
            url = f"https://www.google.com/search?q={urllib.parse.quote(query)}&num={num_results}"
            response = self._http_client.get(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                                  "Chrome/120.0.0.0 Safari/537.36",
                    "Accept": "text/html",
                },
            )

            if response.status_code == 200:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.text, "html.parser")
                results = []

                for g in soup.select("div.g")[:num_results]:
                    title_elem = g.select_one("h3")
                    link_elem = g.select_one("a")
                    snippet_elem = g.select_one("div.VwiC3b")

                    if title_elem and link_elem:
                        results.append({
                            "title": title_elem.get_text(strip=True),
                            "url": link_elem.get("href", ""),
                            "snippet": snippet_elem.get_text(strip=True) if snippet_elem else "",
                        })

                return results
        except Exception as e:
            console.print(f"[dim]Google fallback search failed: {e}[/]")

        return []

    def search_earning_opportunities(self, query: str = "") -> list[dict]:
        """Search for specific earning opportunities."""
        search_queries = [
            query or "urgent freelance writing jobs today",
            query or "freelance data entry work from home",
            query or "AI content writing gigs immediate start",
            query or "micro task websites earn money online",
            query or "remote virtual assistant jobs no experience",
        ]

        all_results = []
        for q in search_queries:
            results = self.search(q, num_results=3)
            all_results.extend(results)

        return all_results

    def search_client_contacts(self, industry: str = "") -> list[dict]:
        """Search for potential client contacts."""
        queries = [
            f"small business owners looking for {industry} freelancer",
            f"companies hiring remote {industry} contractor",
            f"freelance {industry} opportunities immediate start",
        ]

        results = []
        for q in queries:
            results.extend(self.search(q, num_results=2))
        return results

    def check_platform_availability(self, platform_url: str) -> bool:
        """Check if a platform website is accessible."""
        try:
            response = self._http_client.get(platform_url, timeout=10)
            return response.status_code == 200
        except Exception:
            return False

    def close(self) -> None:
        """Close the HTTP client."""
        self._http_client.close()
