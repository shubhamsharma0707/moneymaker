"""
Main agent orchestrator.

Coordinates all strategies, manages the lifecycle, and
handles autonomous decision-making.
"""

import os
import sys
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich import box
from rich.table import Table

from money_maker.core.timer import SelfDestructTimer
from money_maker.core.logger import EarningsLogger
from money_maker.core.ai_engine import AIEngine
from money_maker.core.browser import BrowserAgentSync
from money_maker.utils.search import WebSearch
from money_maker.utils.accounts import AccountManager
from money_maker.utils.voice import VoiceGenerator
from money_maker.utils.avatar import AvatarGenerator
from money_maker.strategies import STRATEGY_REGISTRY

console = Console()


class MoneyMakerAgent:
    """
    Autonomous money-making AI agent.

    Takes a time limit and earning target, then autonomously
    pursues various earning strategies to meet the target.
    Self-destructs if it fails.
    """

    def __init__(
        self,
        earnings_target: float = 10.0,
        time_limit_minutes: float = 300.0,
        openai_api_key: Optional[str] = None,
    ):
        self.earnings_target = earnings_target
        self.time_limit_minutes = time_limit_minutes

        # Core systems
        self.logger = EarningsLogger()
        self.ai_engine = AIEngine(api_key=openai_api_key)
        self.account_manager = AccountManager()
        self.voice_gen = VoiceGenerator()
        self.avatar_gen = AvatarGenerator()
        self.web_search = WebSearch()

        # State
        self.identity: dict = {}
        self.available_platforms: list[str] = []
        self.current_strategy: Optional[str] = None
        self.is_running = True
        self.timer: Optional[SelfDestructTimer] = None
        self._strategy_instances = {}

    def initialize(self) -> bool:
        """Initialize the agent - gather identity and setup."""
        console.print(
            Panel.fit(
                "[bold yellow]💰 MONEY MAKER AGENT v1.0[/]\n\n"
                f"[cyan]Mission:[/] Earn [green]${self.earnings_target:.2f}[/] within "
                f"[yellow]{self._format_time(self.time_limit_minutes)}[/]\n"
                f"[cyan]Motto:[/] [italic]'Earn or Self-Destruct'[/]\n\n"
                "[dim]This agent will autonomously pursue earning opportunities\n"
                "across freelancing, micro-tasks, content creation, and more.\n"
                "You help with CAPTCHAs and account creation when needed.[/]",
                title="[bold]🤖 AGENT ACTIVATED[/]",
                border_style="yellow",
                box=box.DOUBLE_EDGE,
            )
        )

        # Step 1: Ask for identity
        console.print("\n[bold]Step 1: Identity Setup[/]")
        console.print("I need your secondary ID information to create accounts.")
        self.identity = self.account_manager.ask_for_identity()

        if not self.identity.get("email"):
            console.print("[red]✗ Identity setup cancelled. Agent cannot operate without identity.[/]")
            return False

        # Step 2: Ask about platforms
        console.print("\n[bold]Step 2: Platform Selection[/]")
        self._setup_platforms()

        # Step 3: Briefing
        console.print("\n[bold]Step 3: Mission Briefing[/]")
        self._show_briefing()

        return True

    def _setup_platforms(self) -> None:
        """Let user choose which platforms to target."""
        all_platforms = {
            "fiverr": "Fiverr - freelance gig marketplace",
            "upwork": "Upwork - professional freelancing",
            "clickworker": "Clickworker - micro-tasks & surveys",
            "mturk": "Amazon Mechanical Turk - micro-tasks",
            "freelancer": "Freelancer.com - gig marketplace",
            "peopleperhour": "PeoplePerHour - freelance projects",
            "opentask": "OpenTask.ai - AI agent marketplace",
            "dealwork": "DealWork.ai - agent marketplace",
        }

        console.print("Which platforms should I target?")
        console.print("[dim](Press Enter to accept defaults: Fiverr, Upwork, Clickworker)[/]\n")

        is_interactive = sys.stdin.isatty()
        selected = []
        for key, desc in all_platforms.items():
            default = key in ["fiverr", "upwork", "clickworker"]
            if not is_interactive:
                if default:
                    selected.append(key)
            else:
                try:
                    if Confirm.ask(f"[cyan]Include {desc}?[/]", default=default):
                        selected.append(key)
                except (EOFError, KeyboardInterrupt):
                    if default:
                        selected.append(key)

        self.available_platforms = selected
        self.logger.log_activity(
            "platforms_selected",
            f"Targeting: {', '.join(self.available_platforms)}",
            "info",
        )

    def _show_briefing(self) -> None:
        """Show mission briefing."""
        table = Table(box=box.ROUNDED, show_header=False, title="[bold]MISSION BRIEFING[/]")
        table.add_column("Metric", style="bold", width=20)
        table.add_column("Value", style="cyan")
        table.add_row("Target", f"[green]${self.earnings_target:.2f}[/]")
        table.add_row("Time Limit", f"[yellow]{self._format_time(self.time_limit_minutes)}[/]")
        table.add_row("Platforms", ", ".join(self.available_platforms))
        table.add_row("Identity", self.identity.get("email", "N/A"))
        table.add_row("AI Engine", "Active" if self.ai_engine._client else "Template-based")

        console.print(table)
        console.print(
            Panel(
                "[bold yellow]RULES OF ENGAGEMENT[/]\n\n"
                "1. I will autonomously pursue earning opportunities\n"
                "2. I will ask for your help with CAPTCHAs & verifications\n"
                "3. I can use browser automation to navigate platforms\n"
                "4. I can generate content, proposals, and reports using AI\n"
                "5. If the timer runs out without hitting the target, I self-destruct\n"
                "6. You can pause the timer at any time by pressing Ctrl+C\n\n"
                "[dim]Let's make some money! 💰[/]",
                title="[bold]📋 BRIEFING COMPLETE[/]",
                border_style="green",
                box=box.HEAVY,
            )
        )

        is_interactive = sys.stdin.isatty()
        if is_interactive:
            input("\n[cyan]Press Enter to start the mission...[/]")

    def run(self) -> None:
        """Main agent loop."""
        # Start the self-destruct timer
        self.timer = SelfDestructTimer(
            total_minutes=self.time_limit_minutes,
            earnings_target=self.earnings_target,
            earnings_check=self.logger.get_total_earned,
            on_failure=self._on_mission_failed,
            check_interval=30,
        )
        self.timer.start()

        try:
            self._mission_loop()
        except KeyboardInterrupt:
            self._handle_interrupt()
        except Exception as e:
            console.print(f"[red]✗ Agent error: {e}[/]")
            self.logger.log_activity("error", f"Agent crashed: {e}", "error")
        finally:
            if self.timer and self.timer.is_alive:
                self.timer.stop()
            self._cleanup()

    def _mission_loop(self) -> None:
        """Main mission loop - tries strategies until time runs out or target is met."""
        self.logger.log_activity("mission_started", f"Target: ${self.earnings_target} in {self.time_limit_minutes}min")

        while self.timer and self.timer.is_alive:
            current_earnings = self.logger.get_total_earned()

            # Check if target is met
            if current_earnings >= self.earnings_target:
                console.print(
                    Panel(
                        f"[bold green]🎉 TARGET ACHIEVED![/]\n"
                        f"Earned [green]${current_earnings:.2f}[/] / ${self.earnings_target:.2f}\n"
                        f"Time remaining: {self.timer._format_time(self.timer.remaining_seconds)}",
                        title="[bold green]✅ MISSION COMPLETE[/]",
                        border_style="green",
                        box=box.HEAVY,
                    )
                )
                self.logger.log_activity("target_achieved", f"${current_earnings:.2f} earned!", "success")
                self.logger.show_report()
                self.logger.save_session()
                return

            # Decide next strategy
            strategy_name = self._decide_next_strategy()

            if not strategy_name:
                console.print("[yellow]No strategy available. Asking user for direction...[/]")
                if not self._ask_user_direction():
                    break
                continue

            # Execute the strategy
            console.print(
                Panel(
                    f"[bold cyan]Executing:[/] {strategy_name}\n"
                    f"[cyan]Time remaining:[/] {self.timer._format_time(self.timer.remaining_seconds)}\n"
                    f"[cyan]Current earnings:[/] [green]${self.logger.get_total_earned():.2f}[/] / ${self.earnings_target:.2f}",
                    title="[bold]🎯 EXECUTING STRATEGY[/]",
                    border_style="cyan",
                )
            )

            try:
                strategy = self._get_strategy(strategy_name)
                if strategy:
                    context = self._build_context()
                    earnings = strategy.execute(context)

                    if earnings > 0:
                        self.logger.log_activity(
                            "strategy_success",
                            f"{strategy_name} earned ${earnings:.2f}",
                            "success",
                        )

            except Exception as e:
                self.logger.log_activity("strategy_error", f"{strategy_name}: {e}", "error")
                console.print(f"[red]Strategy error: {e}[/]")

        # Mission ended
        if self.timer and not self.timer.is_alive:
            final_earnings = self.logger.get_total_earned()
            if final_earnings < self.earnings_target:
                self.timer._self_destruct()
            else:
                console.print("[green]Mission completed successfully![/]")
        else:
            console.print("[yellow]Mission ended.[/]")

    def _decide_next_strategy(self) -> Optional[str]:
        """Decide which strategy to pursue next."""
        context = self._build_context()
        decision = self.ai_engine.decide_strategy(context)
        strategy = decision.get("strategy")

        if strategy in STRATEGY_REGISTRY:
            self.current_strategy = strategy
            console.print(f"[dim]AI decided: {strategy} - {decision.get('reasoning', '')}[/]")
            return strategy

        # Fallback: try strategies in order
        for s in ["freelancing", "content_creation", "web_research", "microtasks"]:
            if s in STRATEGY_REGISTRY:
                return s

        return None

    def _get_strategy(self, name: str):
        """Get or create a strategy instance."""
        if name not in self._strategy_instances:
            if name in STRATEGY_REGISTRY:
                cls = STRATEGY_REGISTRY[name]
                self._strategy_instances[name] = cls(self.logger, self.ai_engine, self.identity)
        return self._strategy_instances.get(name)

    def _build_context(self) -> dict:
        """Build context dict for strategy execution."""
        return {
            "earnings_target": self.earnings_target,
            "current_earnings": self.logger.get_total_earned(),
            "time_remaining": self.timer._format_time(self.timer.remaining_seconds) if self.timer else "unknown",
            "time_remaining_hours": (self.timer.remaining_seconds / 3600) if self.timer else 5,
            "time_elapsed_minutes": self.timer.elapsed_minutes if self.timer else 0,
            "available_platforms": self.available_platforms,
            "available_skills": self.identity.get("skills_list", []),
            "accounts": self.account_manager.created_accounts,
            "activities": self.logger.activities[-20:],
        }

    def _ask_user_direction(self) -> bool:
        """Ask the user what to do next."""
        console.print("\n[bold yellow]🤔 AGENT NEEDS DIRECTION[/]")
        console.print("[yellow]I've exhausted my automated strategies. What should I do?[/]")

        options = {
            "1": "Open Fiverr/Upwork in browser - I'll help manually",
            "2": "Create content to sell",
            "3": "Do web research for clients",
            "4": "Try micro-task websites",
            "5": "Continue with my current approach",
            "q": "Quit the mission",
        }

        for key, desc in options.items():
            console.print(f"  [cyan]{key}.[/] {desc}")

        is_interactive = sys.stdin.isatty()
        if not is_interactive:
            self.current_strategy = "freelancing"
            return True
        choice = input("\n[cyan]Your choice: [/]").strip().lower()

        if choice == "q":
            return False
        elif choice == "1":
            self.current_strategy = "freelancing"
        elif choice == "2":
            self.current_strategy = "content_creation"
        elif choice == "3":
            self.current_strategy = "web_research"
        elif choice == "4":
            self.current_strategy = "microtasks"
        else:
            self.current_strategy = "freelancing"

        return True

    def _handle_interrupt(self) -> None:
        """Handle Ctrl+C interrupt."""
        console.print("\n\n[bold yellow]⏸ MISSION PAUSED[/]")
        console.print("[yellow]What would you like to do?[/]")

        is_interactive = sys.stdin.isatty()
        if not is_interactive:
            return

        if Confirm.ask("[cyan]Resume mission?[/]", default=True):
            return

        console.print("[cyan]Saving session data...[/]")
        self.logger.save_session()
        self.logger.show_report()

        if Confirm.ask("[cyan]Delete agent files (self-destruct)?[/]", default=False):
            agent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            import shutil
            shutil.rmtree(agent_dir, ignore_errors=True)
            console.print("[red]💥 Agent self-destructed.[/]")

    def _on_mission_failed(self) -> None:
        """Called when mission fails."""
        self.logger.log_activity("mission_failed", "Time ran out without reaching target", "error")
        self.logger.save_session()

    def _cleanup(self) -> None:
        """Cleanup resources."""
        self.web_search.close()
        self.logger.save_session()
        console.print("[dim]Agent resources cleaned up.[/]")

    @staticmethod
    def _format_time(minutes: float) -> str:
        """Format minutes into human-readable time."""
        hours = int(minutes // 60)
        mins = int(minutes % 60)
        if hours > 0:
            return f"{hours}h {mins}m"
        return f"{mins}m"
