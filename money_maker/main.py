#!/usr/bin/env python3
"""
Money Maker Agent - Autonomous AI-powered earning system.

Usage:
    python main.py --target 10 --time 5

The agent will autonomously pursue earning opportunities and
self-destructs if it fails to meet the target within the time limit.
"""

import os
import sys
import argparse
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich import box

# Load .env file
load_dotenv()

# Create single data directory
DATA_DIR = os.path.expanduser("~/.money_maker")
os.makedirs(DATA_DIR, exist_ok=True)

console = Console()

BANNER = """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   ███╗   ███╗ ██████╗ ███╗   ██╗███████╗██╗   ██╗            ║
║   ████╗ ████║██╔═══██╗████╗  ██║██╔════╝╚██╗ ██╔╝            ║
║   ██╔████╔██║██║   ██║██╔██╗ ██║█████╗   ╚████╔╝             ║
║   ██║╚██╔╝██║██║   ██║██║╚██╗██║██╔══╝    ╚██╔╝              ║
║   ██║ ╚═╝ ██║╚██████╔╝██║ ╚████║███████╗   ██║               ║
║   ╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝   ╚═╝               ║
║                                                               ║
║    █████╗  ██████╗ ███████╗███╗   ██╗████████╗                ║
║   ██╔══██╗██╔════╝ ██╔════╝████╗  ██║╚══██╔══╝                ║
║   ███████║██║  ███╗█████╗  ██╔██╗ ██║   ██║                   ║
║   ██╔══██║██║   ██║██╔══╝  ██║╚██╗██║   ██║                   ║
║   ██║  ██║╚██████╔╝███████╗██║ ╚████║   ██║                   ║
║   ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝                   ║
║                                                               ║
║            💰 EARN OR SELF-DESTRUCT 💰                        ║
║           (DEMO / SIMULATION MODE ONLY)                       ║
╚═══════════════════════════════════════════════════════════════╝
"""


def setup_environment():
    """Setup environment and check dependencies."""
    # Check for .env file
    env_path = Path(__file__).parent / ".env"
    if not env_path.exists():
        console.print("[yellow]⚠ No .env file found. Creating template...[/]")
        template = """# Money Maker Agent Configuration
# Get your OpenAI API key from: https://platform.openai.com/api-keys
OPENAI_API_KEY=your_key_here

# Optional: ElevenLabs API key (for voice generation)
# Get free tier: https://elevenlabs.io/
ELEVENLABS_API_KEY=

# Optional: Your preferred AI model
# Options: gpt-4o-mini (default, cheap), gpt-4o (better), gpt-3.5-turbo (cheapest)
AI_MODEL=gpt-4o-mini
"""
        env_path.write_text(template)
        console.print("[green]✓ .env template created! Edit it with your API key.[/]")
        return False

    return True


def check_playwright():
    """Check if Playwright browsers are installed."""
    try:
        from playwright.sync_api import sync_playwright
        return True
    except ImportError:
        return False


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Money Maker Agent - Autonomous AI earning system",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --target 10 --time 5     # Earn $10 in 5 hours
  python main.py --target 50 --time 24    # Earn $50 in 24 hours
  python main.py --target 5 --time 1      # Earn $5 in 1 hour
        """,
    )

    parser.add_argument(
        "--target", "-t",
        type=float,
        default=None,
        help="Amount of money to earn (in USD). Example: --target 10",
    )
    parser.add_argument(
        "--time", "-m",
        type=float,
        default=None,
        help="Time limit in hours. Example: --time 5 for 5 hours",
    )
    parser.add_argument(
        "--minutes",
        type=float,
        default=None,
        help="Time limit in minutes. Alternative to --time",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run browser in headless mode",
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Disable browser automation (content/strategy only)",
    )
    parser.add_argument(
        "--api-key",
        default=None,
        help="OpenAI API key (overrides .env)",
    )
    parser.add_argument(
        "--yes", "-y",
        action="store_true",
        help="Non-interactive mode - use defaults for all prompts",
    )

    args = parser.parse_args()

    # Non-interactive mode helpers
    is_interactive = sys.stdin.isatty() and not args.yes

    def safe_confirm(prompt_text: str, default: bool = True) -> bool:
        """Handle confirm prompts in both interactive and non-interactive modes."""
        if not is_interactive:
            return default
        try:
            return Confirm.ask(prompt_text, default=default)
        except (EOFError, KeyboardInterrupt):
            return default

    def safe_prompt(prompt_text: str, default: str = "") -> str:
        """Handle text prompts in both interactive and non-interactive modes."""
        if not is_interactive:
            return default
        try:
            return Prompt.ask(prompt_text, default=default)
        except (EOFError, KeyboardInterrupt):
            return default

    # Show banner
    console.print(BANNER, style="cyan", justify="center")

    # Setup
    env_ready = setup_environment()
    if not env_ready:
        console.print(
            "\n[bold yellow]⚙  FIRST TIME SETUP[/]"
            "\n1. Edit the .env file with your OpenAI API key"
            "\n2. Install dependencies: pip install -r requirements.txt"
            "\n3. Install Playwright: playwright install chromium"
            "\n4. Run the agent again!"
        )
        sys.exit(0)

    # Playwright check
    if not args.no_browser and not check_playwright():
        console.print(
            "[yellow]⚠ Playwright not fully installed.[/]\n"
            "Run: [bold]pip install playwright && playwright install chromium[/]"
        )
        if not safe_confirm("[cyan]Continue without browser automation?[/]", default=True):
            sys.exit(0)

    # Get target amount
    target = args.target
    if target is None:
        console.print("\n[bold cyan]💰 SETUP: Earnings Target[/]")
        console.print("[dim]How much do you want to earn?[/]")
        target = float(Prompt.ask("[cyan]Target amount ($)[/]", default="10"))
        if target <= 0:
            console.print("[red]Target must be greater than 0![/]")
            sys.exit(1)

    # Get time limit
    if args.time:
        time_limit_minutes = args.time * 60
    elif args.minutes:
        time_limit_minutes = args.minutes
    else:
        console.print("\n[bold cyan]⏱ Auto-Pilot Mode: Setting Time Limit to 5 hours[/]")
        time_hours = 5.0
        time_limit_minutes = time_hours * 60

    if time_limit_minutes <= 0:
        console.print("[red]Time limit must be greater than 0![/]")
        sys.exit(1)

    # Get API key
    api_key = args.api_key or os.environ.get("OPENAI_API_KEY", "")

    # Confirm
    console.print(
        Panel(
            f"[bold]Mission Parameters[/]\n\n"
            f"Target: [green]${target:.2f}[/]\n"
            f"Time: [yellow]{time_limit_minutes / 60:.1f}h ({time_limit_minutes:.0f}min)[/]\n"
            f"Browser: [cyan]{'Enabled' if not args.no_browser else 'Disabled'}[/]\n"
            f"AI Engine: [cyan]{'GPT-4o-mini' if api_key else 'Template-based (limited)'}[/]",
            title="[bold]🎯 MISSION PARAMETERS[/]",
            border_style="cyan",
            box=box.DOUBLE_EDGE,
        )
    )

    console.print("\n[bold yellow]🚀 Auto-Pilot Launching Agent...[/]")

    # Create and run the agent
    try:
        from money_maker.core.agent import MoneyMakerAgent

        agent = MoneyMakerAgent(
            earnings_target=target,
            time_limit_minutes=time_limit_minutes,
            openai_api_key=api_key,
        )

        if agent.initialize():
            agent.run()
        else:
            console.print("[red]✗ Agent initialization failed.[/]")
            sys.exit(1)

    except KeyboardInterrupt:
        console.print("\n[yellow]Mission terminated by user.[/]")
    except Exception as e:
        console.print(f"\n[red]✗ Fatal error: {e}[/]")
        import traceback
        console.print(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()
