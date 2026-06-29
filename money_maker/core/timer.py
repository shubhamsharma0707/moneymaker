"""
Countdown timer with self-destruct mechanism.

The agent is given a time limit to earn a target amount.
If it fails, it deletes itself (agent "dies").
"""

import os
import shutil
import time
import threading
from datetime import datetime
from typing import Callable, Optional

from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
from rich.text import Text
from rich import box

console = Console()

SELF_DESTRUCT_MESSAGE = """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   💀  AGENT TERMINATED - MISSION FAILED  💀                   ║
║                                                               ║
║   The agent failed to earn the target amount within the       ║
║   given time. Self-destruct sequence initiated.               ║
║                                                               ║
║   All agent files have been deleted.                          ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
"""


class SelfDestructTimer:
    """Countdown timer that triggers self-destruct on failure."""

    def __init__(
        self,
        total_minutes: float,
        earnings_target: float,
        earnings_check: Callable[[], float],
        on_failure: Optional[Callable] = None,
        check_interval: int = 10,
        agent_dir: str = None,
    ):
        self.total_seconds = total_minutes * 60
        self.remaining_seconds = self.total_seconds
        self.earnings_target = earnings_target
        self.earnings_check = earnings_check
        self.on_failure = on_failure
        self.check_interval = check_interval
        self.agent_dir = agent_dir or os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )
        self._running = False
        self._paused = False
        self._start_time: Optional[float] = None
        self._thread: Optional[threading.Thread] = None

    def start(self) -> None:
        """Start the countdown timer."""
        self._running = True
        self._start_time = time.time()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        console.print(
            Panel(
                f"[bold yellow]⏱ Timer Started:[/] [cyan]{self._format_time(self.total_seconds)}[/]\n"
                f"[bold yellow]🎯 Target:[/] [green]${self.earnings_target:.2f}[/]\n"
                f"[dim]Agent must earn this amount before time runs out or it will self-destruct.[/]",
                title="[bold red]💰 MONEY MAKER AGENT[/]",
                border_style="red",
                box=box.HEAVY,
            )
        )

    def pause(self) -> None:
        """Pause the timer."""
        self._paused = True
        console.print("[yellow]⏸ Timer paused (waiting for user input)[/]")

    def resume(self) -> None:
        """Resume the timer."""
        self._paused = False
        console.print("[green]▶ Timer resumed[/]")

    def stop(self) -> None:
        """Stop the timer (mission complete)."""
        self._running = False
        elapsed = time.time() - self._start_time if self._start_time else 0
        console.print(
            Panel(
                f"[bold green]✅ MISSION COMPLETE![/]\n"
                f"Time elapsed: [cyan]{self._format_time(elapsed)}[/]\n"
                f"Earnings: [green]${self.earnings_check():.2f}[/] / [green]${self.earnings_target:.2f}[/]",
                title="[bold green]SUCCESS[/]",
                border_style="green",
            )
        )

    @property
    def is_alive(self) -> bool:
        """Check if the agent is still alive."""
        return self._running and self.remaining_seconds > 0

    @property
    def elapsed_minutes(self) -> float:
        """Get elapsed time in minutes."""
        if self._start_time:
            return (time.time() - self._start_time) / 60
        return 0

    def get_status(self) -> dict:
        """Get current status."""
        return {
            "remaining": self.remaining_seconds,
            "elapsed": time.time() - self._start_time if self._start_time else 0,
            "earned": self.earnings_check(),
            "target": self.earnings_target,
            "alive": self.is_alive,
        }

    def _run(self) -> None:
        """Internal timer loop."""
        while self._running and self.remaining_seconds > 0:
            if self._paused:
                time.sleep(1)
                continue

            elapsed = time.time() - self._start_time if self._start_time else 0
            self.remaining_seconds = max(0, self.total_seconds - elapsed)
            current_earnings = self.earnings_check()

            # Check if target met
            if current_earnings >= self.earnings_target:
                self.stop()
                return

            # Print periodic status
            if int(elapsed) % 60 == 0 and elapsed > 0:
                self._print_status(current_earnings)

            time.sleep(self.check_interval)

        # Time's up - trigger self-destruct
        if self.remaining_seconds <= 0 and self._running:
            self._running = False
            current_earnings = self.earnings_check()
            if current_earnings < self.earnings_target:
                self._self_destruct()
            else:
                self.stop()

    def _self_destruct(self) -> None:
        """Self-destruct: delete agent files."""
        console.print("[bold red]⏰ TIME'S UP![/]")
        console.print(SELF_DESTRUCT_MESSAGE, style="bold red", justify="center")

        if self.on_failure:
            self.on_failure()

        # Log the failure before deleting
        try:
            log_dir = os.path.join(os.path.expanduser("~"), ".money_maker_logs")
            os.makedirs(log_dir, exist_ok=True)
            with open(os.path.join(log_dir, "failure_log.txt"), "a") as f:
                f.write(
                    f"Mission failed at {datetime.now().isoformat()}: "
                    f"Earned ${self.earnings_check():.2f} / ${self.earnings_target:.2f}\n"
                )
        except Exception:
            pass

        # Delete agent files
        try:
            if os.path.exists(self.agent_dir):
                shutil.rmtree(self.agent_dir, ignore_errors=True)
                console.print("[bold red]💥 Agent files destroyed.[/]")
        except Exception as e:
            console.print(f"[red]Warning: Could not fully self-destruct: {e}[/]")

        os._exit(0)

    def _print_status(self, current_earnings: float) -> None:
        """Print status update."""
        progress = min(1.0, current_earnings / self.earnings_target) if self.earnings_target > 0 else 0
        bar_length = 30
        filled = int(bar_length * progress)
        bar = "█" * filled + "░" * (bar_length - filled)

        status = Table(box=box.SIMPLE, show_header=False)
        status.add_column(style="bold", width=15)
        status.add_column(style="cyan")
        status.add_row("⏱ Remaining", self._format_time(self.remaining_seconds))
        status.add_row("💰 Earned", f"${current_earnings:.2f}")
        status.add_row("🎯 Target", f"${self.earnings_target:.2f}")
        status.add_row("📊 Progress", f"[green]{bar}[/] ({progress * 100:.1f}%)")

        console.print(Panel(status, title="[bold]AGENT STATUS[/]", border_style="cyan"))

    @staticmethod
    def _format_time(seconds: float) -> str:
        """Format seconds into human-readable time."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        if hours > 0:
            return f"{hours}h {minutes}m {secs}s"
        return f"{minutes}m {secs}s"
