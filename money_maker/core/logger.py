"""
Session logging and earnings tracking.

Tracks all agent activities, earnings, and provides status reporting.
"""

import json
import os
from datetime import datetime
from typing import Optional
from pathlib import Path

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from rich.layout import Layout
from rich.text import Text

console = Console()


class EarningsLogger:
    """Tracks earnings and agent activities."""

    def __init__(self, session_id: Optional[str] = None):
        self.session_id = session_id or datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_dir = Path.home() / ".money_maker_logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.session_file = self.log_dir / f"session_{self.session_id}.json"
        self.earnings_file = self.log_dir / "earnings_total.json"

        self.activities: list[dict] = []
        self.earnings: list[dict] = []
        self.total_earned: float = 0.0
        self._load_persistent_earnings()

        # Activity log file
        self.activity_file = self.log_dir / f"activities_{self.session_id}.log"

    def _load_persistent_earnings(self) -> None:
        """Load cumulative earnings from persistent storage."""
        if self.earnings_file.exists():
            try:
                data = json.loads(self.earnings_file.read_text())
                self.total_earned = data.get("total_earned", 0.0)
            except (json.JSONDecodeError, KeyError):
                self.total_earned = 0.0

    def _save_persistent_earnings(self) -> None:
        """Save cumulative earnings."""
        data = {
            "total_earned": self.total_earned,
            "last_updated": datetime.now().isoformat(),
            "last_session": self.session_id,
        }
        self.earnings_file.write_text(json.dumps(data, indent=2))

    def log_activity(self, action: str, details: str = "", status: str = "info") -> None:
        """Log an activity."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "details": details,
            "status": status,
        }
        self.activities.append(entry)

        # Color code status
        status_colors = {"info": "blue", "success": "green", "warning": "yellow", "error": "red"}
        color = status_colors.get(status, "white")
        console.print(f"  [{color}]•[/] [{color}]{action}[/]: {details}")

        # Write to activity file
        with open(self.activity_file, "a") as f:
            f.write(f"[{entry['timestamp']}] [{status.upper()}] {action}: {details}\n")

    def log_earning(self, amount: float, source: str, description: str = "") -> None:
        """Log an earning event."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "amount": amount,
            "source": source,
            "description": description,
        }
        self.earnings.append(entry)
        self.total_earned += amount
        self._save_persistent_earnings()

        console.print(
            f"  [bold green]💰 +${amount:.2f}[/] from [cyan]{source}[/]"
            + (f" - {description}" if description else "")
        )

    def get_total_earned(self) -> float:
        """Get total earnings across all sessions."""
        return self.total_earned

    def get_session_earnings(self) -> float:
        """Get earnings for this session only."""
        return sum(e["amount"] for e in self.earnings)

    def show_report(self) -> None:
        """Display a comprehensive earnings report."""
        layout = Layout()

        # Summary
        summary = Table(box=box.ROUNDED, show_header=False, title="[bold]SESSION SUMMARY[/]")
        summary.add_column(style="bold", width=20)
        summary.add_column(style="cyan")
        summary.add_row("Session ID", self.session_id)
        summary.add_row("Session Earnings", f"[green]${self.get_session_earnings():.2f}[/]")
        summary.add_row("All-Time Earnings", f"[green]${self.total_earned:.2f}[/]")
        summary.add_row("Activities", str(len(self.activities)))

        console.print(Panel(summary, title="[bold]📊 EARNINGS REPORT[/]", border_style="green"))

        # Recent earnings
        if self.earnings:
            earnings_table = Table(
                box=box.SIMPLE,
                show_header=True,
                header_style="bold cyan",
                title="[bold]EARNINGS LOG[/]",
            )
            earnings_table.add_column("Time", style="dim")
            earnings_table.add_column("Amount", style="green")
            earnings_table.add_column("Source", style="cyan")
            earnings_table.add_column("Description")

            for e in self.earnings[-10:]:  # Last 10 entries
                earnings_table.add_row(
                    e["timestamp"][11:19],
                    f"${e['amount']:.2f}",
                    e["source"],
                    e.get("description", ""),
                )
            console.print(earnings_table)

    def save_session(self) -> None:
        """Save session data to file."""
        data = {
            "session_id": self.session_id,
            "started": self.activities[0]["timestamp"] if self.activities else datetime.now().isoformat(),
            "activities": self.activities,
            "earnings": self.earnings,
            "session_total": self.get_session_earnings(),
            "total_earned": self.total_earned,
        }
        self.session_file.write_text(json.dumps(data, indent=2))
        self.log_activity("session_saved", f"Session data saved to {self.session_file}")
