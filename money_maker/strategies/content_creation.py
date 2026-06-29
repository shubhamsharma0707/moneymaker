"""
Content creation strategy.

Offers AI-powered content writing services:
- Blog posts & articles
- Copywriting & marketing copy
- Product descriptions
- Social media content
- Email newsletters
- Script writing
"""

from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich import box

from money_maker.strategies.base import BaseStrategy

console = Console()

CONTENT_SERVICES = {
    "blog_post": {
        "name": "Blog Post / Article",
        "word_count": 800,
        "time_min": 30,
        "price": 12,
        "description": "SEO-optimized blog post or article",
    },
    "product_description": {
        "name": "Product Description (5 items)",
        "word_count": 500,
        "time_min": 20,
        "price": 8,
        "description": "Compelling product descriptions for e-commerce",
    },
    "social_media": {
        "name": "Social Media Content Pack (10 posts)",
        "word_count": 500,
        "time_min": 25,
        "price": 10,
        "description": "Engaging social media posts with captions",
    },
    "email_newsletter": {
        "name": "Email Newsletter",
        "word_count": 600,
        "time_min": 25,
        "price": 10,
        "description": "Professional email newsletter content",
    },
    "script": {
        "name": "Video Script (2-3 min)",
        "word_count": 400,
        "time_min": 30,
        "price": 15,
        "description": "Engaging video script with hook and CTA",
    },
    "copywriting": {
        "name": "Landing Page Copy",
        "word_count": 400,
        "time_min": 35,
        "price": 15,
        "description": "Conversion-optimized landing page text",
    },
}


class ContentCreationStrategy(BaseStrategy):
    """Create and sell content using AI assistance."""

    def execute(self, context: dict) -> float:
        """Execute content creation strategy."""
        earnings = 0.0

        self.log("started", "Content creation strategy - offering AI-powered writing services", "info")

        # Show available services
        console.print(Panel(
            "[bold cyan]Available Content Services[/]\n\n" +
            "\n".join([
                f"  [bold]{k}:[/] {v['name']} - [green]${v['price']}[/] (~{v['time_min']}min)"
                for k, v in CONTENT_SERVICES.items()
            ]) +
            "\n\n[dim]AI generates the content, you deliver it to clients.[/]",
            title="[bold]📝 CONTENT SERVICES[/]",
            border_style="cyan",
            box=box.HEAVY,
        ))

        # Let user choose a service
        service_keys = list(CONTENT_SERVICES.keys())
        console.print("\n[cyan]Choose a service to fulfill (or fulfill an existing order):[/]")
        for i, key in enumerate(service_keys, 1):
            s = CONTENT_SERVICES[key]
            console.print(f"  {i}. {s['name']} - [green]${s['price']}[/] ({s['time_min']}min)")

        choice = Prompt.ask(
            "[cyan]Enter number (1-6)[/]",
            default="1",
        )

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(service_keys):
                service_key = service_keys[idx]
                service = CONTENT_SERVICES[service_key]
                earnings += self._fulfill_content_service(service)
        except (ValueError, IndexError):
            self.log("error", "Invalid choice", "error")

        # Offer to do more
        if earnings > 0 and Confirm.ask("[cyan]Create more content?[/]", default=False):
            for key in service_keys:
                s = CONTENT_SERVICES[key]
                if Confirm.ask(f"[cyan]Create {s['name']} (${s['price']})?[/]", default=False):
                    earnings += self._fulfill_content_service(s)

        return earnings

    def _fulfill_content_service(self, service: dict) -> float:
        """Fulfill a content service order."""
        console.print(f"\n[bold]📝 Creating: {service['name']}[/]")
        console.print(f"   Target: ~{service['word_count']} words")
        console.print(f"   Price: [green]${service['price']}[/]")

        # Get topic from user
        topic = Prompt.ask("[cyan]What's the topic?[/]")

        self.log("generating", f"AI generating {service['name']} about '{topic}'", "info")

        # Generate content using AI
        content = self.ai.generate_content(topic, service["name"], service["word_count"])

        # Save content to file
        import os
        from datetime import datetime

        output_dir = os.path.expanduser("~/.money_maker_content")
        os.makedirs(output_dir, exist_ok=True)

        filename = f"{topic.lower().replace(' ', '_')[:30]}_{datetime.now().strftime('%H%M%S')}.md"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, "w") as f:
            f.write(f"# {topic}\n\n")
            f.write(f"Type: {service['name']}\n")
            f.write(f"Created: {datetime.now().isoformat()}\n")
            f.write(f"Price: ${service['price']}\n")
            f.write(f"\n---\n\n")
            f.write(content)

        # Show preview
        preview = content[:300] + "..." if len(content) > 300 else content
        console.print(f"\n[bold]📄 Preview:[/]")
        console.print(f"[dim]{preview}[/]")
        console.print(f"\n[green]✓ Content saved to: {filepath}[/]")

        # Ask if delivered to client
        if Confirm.ask("[cyan]Did you deliver this to a client?[/]", default=True):
            client = Prompt.ask("[cyan]Client name/platform?[/]", default="direct")
            self.log_earning(service["price"], f"Content: {service['name']}", f"Client: {client}")
            self.log("delivered", f"{service['name']} delivered: '{topic}'", "success")
            return service["price"]

        return 0.0

    def estimate_earnings_potential(self, time_minutes: float) -> float:
        """Estimate content creation earnings."""
        avg_service_time = 25  # minutes
        avg_price = 10  # dollars
        num_services = int(time_minutes / avg_service_time)
        return num_services * avg_price
