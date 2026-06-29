"""
Web research strategy.

Offers web research and data collection services:
- Market research reports
- Competitor analysis
- Lead generation (find emails, contacts)
- Data collection and organization
- Fact-checking and verification
"""

from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table

from money_maker.strategies.base import BaseStrategy
from money_maker.utils.search import WebSearch

console = Console()

RESEARCH_SERVICES = [
    {
        "name": "Competitor Analysis (3 companies)",
        "time_min": 30,
        "price": 12,
        "description": "Research competitors' products, pricing, and positioning",
    },
    {
        "name": "Lead Generation (50 leads)",
        "time_min": 25,
        "price": 10,
        "description": "Find emails, LinkedIn profiles, company info",
    },
    {
        "name": "Market Research Report",
        "time_min": 40,
        "price": 15,
        "description": "In-depth research on a specific market or industry",
    },
    {
        "name": "Data Collection (custom)",
        "time_min": 20,
        "price": 8,
        "description": "Collect and organize specific data from the web",
    },
]


class WebResearchStrategy(BaseStrategy):
    """Perform paid web research tasks."""

    def __init__(self, logger, ai_engine, identity):
        super().__init__(logger, ai_engine, identity)
        self.searcher = WebSearch()

    def execute(self, context: dict) -> float:
        """Execute web research strategy."""
        earnings = 0.0

        self.log("started", "Web research strategy - offering data collection services", "info")

        # Show available research services
        table = Table(title="[bold]📊 RESEARCH SERVICES[/]")
        table.add_column("Service", style="cyan")
        table.add_column("Time", style="yellow")
        table.add_column("Price", style="green")
        table.add_column("Description")

        for s in RESEARCH_SERVICES:
            table.add_row(s["name"], f"{s['time_min']}min", f"${s['price']}", s["description"])

        console.print(table)

        # Choose a service
        console.print("\n[cyan]Which research service would you like to fulfill?[/]")
        for i, s in enumerate(RESEARCH_SERVICES, 1):
            console.print(f"  {i}. {s['name']} - [green]${s['price']}[/]")

        choice = Prompt.ask("[cyan]Enter number (1-4)[/]", default="2")

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(RESEARCH_SERVICES):
                service = RESEARCH_SERVICES[idx]
                earnings += self._fulfill_research(service)
        except (ValueError, IndexError):
            self.log("error", "Invalid choice", "error")

        # Cleanup
        self.searcher.close()
        return earnings

    def _fulfill_research(self, service: dict) -> float:
        """Fulfill a research service."""
        topic = Prompt.ask(f"[cyan]Research topic?[/]", default="technology startups")
        self.log("researching", f"Starting {service['name']} on '{topic}'", "info")

        console.print(f"\n[cyan]🔍 AI Agent researching: {topic}[/]")
        console.print(f"   Service: {service['name']}")
        console.print(f"   Price: [green]${service['price']}[/]")

        # Perform the research
        results = self.searcher.search_earning_opportunities(topic)

        # Try to get more specific results based on service type
        if "Lead" in service["name"]:
            additional = self.searcher.search_client_contacts(topic)
            results.extend(additional)

        # Format results into a report
        report_lines = [
            f"# Research Report: {topic}",
            f"Service: {service['name']}",
            f"Generated: {__import__('datetime').datetime.now().isoformat()}",
            "",
            "## Findings",
            "",
        ]

        for r in results[:10]:
            report_lines.append(f"### {r.get('title', 'Result')}")
            report_lines.append(f"URL: {r.get('url', 'N/A')}")
            if r.get("snippet"):
                report_lines.append(f"Summary: {r['snippet']}")
            report_lines.append("")

        report = "\n".join(report_lines)

        # Save report
        import os
        from datetime import datetime

        output_dir = os.path.expanduser("~/.money_maker_research")
        os.makedirs(output_dir, exist_ok=True)

        filename = f"research_{topic.lower().replace(' ', '_')[:20]}_{datetime.now().strftime('%H%M%S')}.md"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, "w") as f:
            f.write(report)

        # Show preview
        preview = report[:400] + "..." if len(report) > 400 else report
        console.print(f"\n[bold]📄 Report Preview:[/]")
        console.print(f"[dim]{preview}[/]")
        console.print(f"\n[green]✓ Full report saved to: {filepath}[/]")

        # Delivery confirmation
        if Confirm.ask("[cyan]Deliver this to client?[/]", default=True):
            client = Prompt.ask("[cyan]Client name/platform?[/]", default="direct")
            self.log_earning(service["price"], service["name"], f"Client: {client}")
            self.log("delivered", f"Research delivered: '{topic}' to {client}", "success")
            return service["price"]

        return 0.0

    def estimate_earnings_potential(self, time_minutes: float) -> float:
        """Estimate research earnings."""
        avg_time = 28  # minutes
        avg_price = 11  # dollars
        num_research = int(time_minutes / avg_time)
        return num_research * avg_price
