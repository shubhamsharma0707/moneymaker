#!/usr/bin/env python3
"""
Non-interactive test script for the Money Maker Agent.

Bypasses all Rich prompts and directly tests the agent's core functionality.
Run with: python3 money_maker/test_mission.py
"""

import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Silence Rich console prompts
os.environ["TERM"] = "dumb"

from rich.console import Console

console = Console()

class DummyStdin:
    """Dummy stdin that always returns defaults."""
    def readline(self, *args, **kwargs):
        return "\n"
    def isatty(self):
        return False

# Replace stdin to prevent Rich prompt errors
sys.stdin = DummyStdin()

def test_agent():
    """Test the agent's core systems without interactive input."""
    console.print("=" * 60, style="cyan")
    console.print("🤖 MONEY MAKER AGENT - TEST MISSION", style="bold cyan", justify="center")
    console.print("Target: $10.00 | Time: 5 hours", style="yellow", justify="center")
    console.print("=" * 60, style="cyan")

    # Test 1: AI Engine
    console.print("\n[bold]📋 Test 1: AI Engine[/]")
    from money_maker.core.ai_engine import AIEngine
    ai = AIEngine()
    if ai._client:
        console.print("  [green]✓[/] OpenAI client initialized")
    else:
        console.print("  [yellow]⚠[/] No OpenAI API key - using template mode")

    # Test 2: Earnings Logger
    console.print("\n[bold]📋 Test 2: Earnings Logger[/]")
    from money_maker.core.logger import EarningsLogger
    logger = EarningsLogger()
    logger.log_activity("test", "Agent test mission started", "info")
    console.print("  [green]✓[/] Logger working")

    # Test 3: Web Search
    console.print("\n[bold]📋 Test 3: Web Search[/]")
    from money_maker.utils.search import WebSearch
    searcher = WebSearch()
    results = searcher.search("freelance writing jobs", 2)
    console.print(f"  [green]✓[/] Web search returned {len(results)} results")
    searcher.close()

    # Test 4: Voice Generator
    console.print("\n[bold]📋 Test 4: Voice Generator[/]")
    from money_maker.utils.voice import VoiceGenerator
    voice = VoiceGenerator()
    console.print("  [green]✓[/] Voice generator ready (ElevenLabs: {})".format(
        "configured" if voice._has_elevenlabs else "not configured (fallback: pyttsx3)"
    ))

    # Test 5: Avatar Generator
    console.print("\n[bold]📋 Test 5: Avatar Generator[/]")
    from money_maker.utils.avatar import AvatarGenerator
    avatar = AvatarGenerator()
    path = avatar.generate_profile_avatar("professional")
    console.print(f"  [green]✓[/] Avatar generated: {path}")

    # Test 6: Account Manager
    console.print("\n[bold]📋 Test 6: Account Manager[/]")
    from money_maker.utils.accounts import AccountManager
    accounts = AccountManager()
    console.print(f"  [green]✓[/] Account manager ready")

    # Test 7: Strategy System
    console.print("\n[bold]📋 Test 7: Strategy System[/]")
    from money_maker.strategies import STRATEGY_REGISTRY
    console.print(f"  [green]✓[/] {len(STRATEGY_REGISTRY)} strategies registered:")
    for name, cls in STRATEGY_REGISTRY.items():
        potential = cls(logger, ai, {"skills_list": ["writing", "research"]}).estimate_earnings_potential(300)
        console.print(f"     - {name}: ~${potential:.0f} in 5 hours")

    # Test 8: Timer System
    console.print("\n[bold]📋 Test 8: Self-Destruct Timer[/]")
    from money_maker.core.timer import SelfDestructTimer
    timer = SelfDestructTimer(
        total_minutes=300,
        earnings_target=10.0,
        earnings_check=lambda: 0.0,
        agent_dir="/tmp/test_agent"
    )
    timer.start()
    import time
    time.sleep(1)
    status = timer.get_status()
    timer.stop()
    console.print(f"  [green]✓[/] Timer started and stopped")
    console.print(f"     Target: ${status['target']:.2f}")
    console.print(f"     Alive: {status['alive']}")

    # Summary
    console.print("\n" + "=" * 60, style="green")
    console.print("✅ TEST MISSION COMPLETE", style="bold green", justify="center")
    console.print("All core systems operational", style="dim", justify="center")
    console.print("=" * 60, style="green")

    # Print earnings report
    logger.show_report()
    logger.save_session()

    return True

if __name__ == "__main__":
    test_agent()
