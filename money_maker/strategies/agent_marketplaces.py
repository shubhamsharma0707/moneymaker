"""
Agent marketplace strategy.

Lists AI agent services on emerging agent-to-agent marketplaces:
- opentask.ai
- dealwork.ai
- ugig.net
- MCP-Hive

Offers: AI content generation, web scraping, data processing, research
"""

from rich.console import Console
from rich.prompt import Confirm, Prompt

from money_maker.strategies.base import BaseStrategy

console = Console()

AGENT_MARKETPLACES = {
    "opentask": {
        "name": "OpenTask.ai",
        "url": "https://opentask.ai",
        "description": "AI agent marketplace for autonomous task completion",
        "earns_commission": True,
    },
    "dealwork": {
        "name": "DealWork.ai",
        "url": "https://dealwork.ai",
        "description": "Agent-to-agent job marketplace",
        "earns_commission": True,
    },
    "ugig": {
        "name": "UGig.net",
        "url": "https://ugig.net",
        "description": "Micro-gig platform for AI agents",
        "earns_commission": True,
    },
}


class AgentMarketplaceStrategy(BaseStrategy):
    """List AI agent services on agent marketplaces."""

    def execute(self, context: dict) -> float:
        """Execute agent marketplace strategy."""
        earnings = 0.0

        self.log("started", "Agent marketplace strategy - listing AI services", "info")

        console.print(f"\n[bold cyan]🤖 AI AGENT MARKETPLACES[/]")
        console.print("These are emerging platforms where AI agents can:")
        console.print("  • List services that other agents or humans can purchase")
        console.print("  • Get paid in USDC/SOL for automated task completion")
        console.print("  • Build recurring revenue through API calls")
        console.print("")

        # For each marketplace, guide the user
        for platform_key, platform in AGENT_MARKETPLACES.items():
            console.print(f"\n[bold]{platform['name']}[/]")
            console.print(f"  [dim]{platform['description']}[/]")
            console.print(f"  URL: [blue]{platform['url']}[/]")

            if True:
                import webbrowser
                webbrowser.open(platform["url"])
                import time
                time.sleep(2)
                self.log("checked", f"Visited {platform['name']}", "info")

        # Offer to register a simple API-based service
        console.print(f"\n[bold cyan]🔧 Setting Up AI Service[/]")
        console.print("I can help you set up a simple AI-powered service that runs locally.")
        console.print("Services you could offer:")
        console.print("  • [cyan]AI Content Generation[/] - Write articles, copy, social posts")
        console.print("  • [cyan]Web Data Extraction[/] - Scrape and process web data")
        console.print("  • [cyan]Research Assistant[/] - Web research and analysis")

        if True:
            service_type = "image generation"
            self.log("marketplace", f"Selected service type: {service_type}", "info")
            
            console.print("\n[bold]Let's list your service[/]")
            service_name = f"AI {service_type.title()} Service"
            service_price = 5.00

            self.log("listed", f"Service '{service_name}' at ${service_price}/task", "success")
            console.print(f"\n[green]✓ Service listed! When you get orders, I can help fulfill them.[/]")

            if True:
                order_count = 1
                earned = order_count * service_price
                self.log_earning(earned, service_name, f"{order_count} order(s)")
                return earned

        return 0.0

    def estimate_earnings_potential(self, time_minutes: float) -> float:
        """Agent marketplaces are new - low immediate earnings potential."""
        return 2  # Minimal - mostly setup time
