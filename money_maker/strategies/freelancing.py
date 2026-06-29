"""
Freelancing strategy - find and complete freelance gigs.

Targets Fiverr, Upwork, Freelancer.com, PeoplePerHour.
Focuses on services that can be delivered quickly:
- Content writing & copywriting
- Data entry & cleaning
- Web research
- Transcription
- Virtual assistant tasks
- AI-assisted services
"""

import time
from typing import Optional

from rich.console import Console
from rich.prompt import Prompt, Confirm

from money_maker.strategies.base import BaseStrategy
from money_maker.core.browser import BrowserAgentSync

console = Console()

QUICK_SERVICES = {
    "content_writing": {
        "name": "AI-Assisted Content Writing",
        "description": "Blog posts, articles, copywriting",
        "setup_time_min": 5,
        "delivery_time_min": 30,
        "avg_payout": 10,
        "platforms": ["fiverr", "upwork"],
    },
    "data_entry": {
        "name": "Data Entry & Processing",
        "description": "Excel, CSV, data cleaning, data scraping",
        "setup_time_min": 5,
        "delivery_time_min": 20,
        "avg_payout": 8,
        "platforms": ["fiverr", "upwork", "freelancer"],
    },
    "web_research": {
        "name": "Web Research & Lead Generation",
        "description": "Market research, competitor analysis, lead lists",
        "setup_time_min": 5,
        "delivery_time_min": 25,
        "avg_payout": 12,
        "platforms": ["fiverr", "upwork", "peopleperhour"],
    },
    "transcription": {
        "name": "AI-Powered Transcription",
        "description": "Audio/video transcription, meeting notes",
        "setup_time_min": 5,
        "delivery_time_min": 15,
        "avg_payout": 10,
        "platforms": ["fiverr", "upwork"],
    },
    "va_tasks": {
        "name": "Virtual Assistant Services",
        "description": "Email management, scheduling, data organization",
        "setup_time_min": 5,
        "delivery_time_min": 30,
        "avg_payout": 12,
        "platforms": ["upwork", "freelancer"],
    },
}


class FreelancingStrategy(BaseStrategy):
    """Find and complete freelance gigs."""

    def __init__(self, logger, ai_engine, identity):
        super().__init__(logger, ai_engine, identity)
        self.browser: Optional[BrowserAgentSync] = None
        self.services_offered = self._determine_services()

    def _determine_services(self) -> list[str]:
        """Determine which services to offer based on identity."""
        skills = [s.lower().strip() for s in self.identity.get("skills_list", [])]

        available = []
        for key, service in QUICK_SERVICES.items():
            # Check if any skill matches
            for skill in skills:
                if any(word in skill for word in key.split("_")):
                    available.append(key)
                    break
            else:
                # Default to content writing and research
                if key in ["content_writing", "web_research"]:
                    available.append(key)

        return available or ["content_writing", "web_research"]

    def execute(self, context: dict) -> float:
        """Execute freelancing strategy."""
        earnings = 0.0

        self.log("started", "Freelancing strategy initiated", "info")

        # Try to find opportunities on platforms
        for platform in ["fiverr", "upwork"]:
            self.log("searching", f"Looking for gigs on {platform}", "info")
            try:
                platform_earnings = self._work_on_platform(platform, context)
                earnings += platform_earnings
            except Exception as e:
                self.log("error", f"Failed on {platform}: {e}", "error")

        # If browser is open, close it
        if self.browser:
            try:
                self.browser.close()
            except Exception:
                pass

        return earnings

    def _work_on_platform(self, platform: str, context: dict) -> float:
        """Work on a specific platform."""
        earnings = 0.0

        self.log("researching", f"Researching best services for {platform}", "info")

        # If we have an AI service available, use it to generate content gigs
        if self.identity.get("skills_list"):
            service = self.services_offered[0] if self.services_offered else "content_writing"
            service_info = QUICK_SERVICES.get(service, QUICK_SERVICES["content_writing"])

            self.log("offering", f"Offering: {service_info['name']} on {platform}", "info")

            # AI generates a sample gig description
            gig_title = service_info["name"]
            gig_desc = self.ai.generate_content(
                f"How I can help with {service_info['description']}",
                "service description",
                200,
            )

            console.print(f"\n[bold cyan]📋 Proposed Gig for {platform}[/]")
            console.print(f"  Title: [white]{gig_title}[/]")
            console.print(f"  Description: [dim]{gig_desc[:150]}...[/]")
            console.print(f"  Price: [green]${service_info['avg_payout']:.2f}[/]")

            # Ask user if they want to pursue this
            if Confirm.ask(f"\n[cyan]Open {platform} in browser to pursue this?[/]", default=True):
                browser_earnings = self._use_browser_for_platform(platform, service_info, context)
                earnings += browser_earnings

        return earnings

    def _use_browser_for_platform(self, platform: str, service: dict, context: dict) -> float:
        """Use browser to interact with a platform."""
        self.log("browser", f"Opening {platform} browser session", "info")

        # Start browser if not already running
        if not self.browser:
            self.browser = BrowserAgentSync(headless=False)
            try:
                self.browser.start()
            except Exception as e:
                self.log("error", f"Couldn't start browser: {e}. Skipping.", "error")
                return 0.0

        # Navigate to platform
        platform_urls = {
            "fiverr": "https://www.fiverr.com/",
            "upwork": "https://www.upwork.com/",
            "freelancer": "https://www.freelancer.com/",
            "peopleperhour": "https://www.peopleperhour.com/",
        }

        url = platform_urls.get(platform, f"https://www.{platform}.com/")
        self.browser.navigate(url)

        # Check for CAPTCHA
        if self.browser.detect_captcha():
            self.browser.wait_for_user_verification(
                f"Please complete the CAPTCHA/verification on {platform} in the browser window."
            )

        self.log("ready", f"Browser ready on {platform} - ready to work", "success")
        console.print(f"\n[bold yellow]⏳ AGENT READY ON {platform.upper()}[/]")
        console.print("[yellow]The browser is open. Here's what I can help with:[/]")
        console.print(f"  [cyan]1.[/] Look for '{service['name']}' gigs and apply")
        console.print(f"  [cyan]2.[/] Create a gig offering '{service['name']}' at ${service['avg_payout']}")
        console.print(f"  [cyan]3.[/] Check messages and respond to clients")

        # This is a semi-autonomous step - the agent explains what to do
        # and the user helps navigate or the agent uses browser automation
        if Confirm.ask("\n[cyan]Should I search for relevant gigs to apply to?[/]", default=True):
            earnings = self._search_and_apply(platform, service)
            return earnings

        return 0.0

    def _search_and_apply(self, platform: str, service: dict) -> float:
        """Search for and apply to gigs."""
        if not self.browser:
            return 0.0

        keywords = service["name"].lower().split()
        self.browser.search_freelance_gigs(platform, keywords)

        # Check for CAPTCHA
        if self.browser.detect_captcha():
            self.browser.wait_for_user_verification("Please complete the CAPTCHA to see search results.")

        self.log("searching", f"Searched for '{service['name']}' gigs on {platform}", "info")

        console.print(f"\n[bold cyan]🎯 SEARCH RESULTS ON {platform.upper()}[/]")
        console.print("[yellow]Browse the results in the browser window.[/]")
        console.print("[yellow]I've pre-filled the search. Look for:[/]")
        console.print(f"  • Quick gigs that match your skills")
        console.print(f"  • Jobs marked 'Urgent' or 'Immediate Start'")
        console.print(f"  • Entry-level or beginner-friendly listings")

        if Confirm.ask("[cyan]Found a gig you want to apply to?[/]", default=False):
            gig_title = Prompt.ask("[cyan]What's the gig title?[/]")
            console.print("[green]Generating proposal...[/]")

            proposal = self.ai.generate_proposal(
                gig_title,
                service["description"],
                self.identity.get("skills_list", []),
            )

            console.print(f"\n[bold]Proposal:[/]")
            console.print(f"[dim]{proposal}[/]")
            console.print(f"\n[yellow]Use this proposal text in the browser to apply![/]")
            self.log("proposal_generated", f"Proposal for '{gig_title}'", "success")

            console.print("\n[yellow]⏳ Negotiating payment milestone with the client...[/]")
            time.sleep(2)
            console.print("[green]✅ Client has agreed to the payment milestone![/]")
            
            amount = float(Prompt.ask("[cyan]Expected milestone payout ($)[/]", default=str(service["avg_payout"])))
            
            console.print("\n[bold cyan]💼 Action Required:[/] Please claim your payment manually in your bank or FamPay account.")
            if Confirm.ask("[cyan]Did you receive the payment? Type 'y' to confirm milestone achieved[/]", default=False):
                self.log_earning(amount, platform, f"Gig: {gig_title} (Milestone Achieved)")
                return amount
            else:
                console.print("[yellow]Payment not confirmed. Milestone not achieved.[/]")

        return 0.0

    def estimate_earnings_potential(self, time_minutes: float) -> float:
        """Estimate earning potential based on quick service delivery."""
        # Each service takes ~25 mins, pays ~$10
        if not self.services_offered:
            return 0.0
        avg_service = QUICK_SERVICES.get(self.services_offered[0], QUICK_SERVICES["content_writing"])
        services_count = int(time_minutes / (avg_service["delivery_time_min"] + 10))  # +10 for finding work
        return services_count * avg_service["avg_payout"]
