"""
Base strategy class for all earning strategies.
"""

from abc import ABC, abstractmethod
from typing import Optional
from money_maker.core.logger import EarningsLogger
from money_maker.core.ai_engine import AIEngine


class BaseStrategy(ABC):
    """Base class for all earning strategies."""

    def __init__(self, logger: EarningsLogger, ai_engine: AIEngine, identity: dict):
        self.logger = logger
        self.ai = ai_engine
        self.identity = identity
        self.name = self.__class__.__name__

    @abstractmethod
    def execute(self, context: dict) -> float:
        """
        Execute the strategy and return earnings.
        """
        pass

    @abstractmethod
    def estimate_earnings_potential(self, time_minutes: float) -> float:
        """
        Estimate how much this strategy could earn in the given time.
        """
        pass

    def log(self, action: str, details: str = "", status: str = "info") -> None:
        """Log an activity."""
        self.logger.log_activity(f"[{self.name}] {action}", details, status)

    def log_earning(self, amount: float, source: str, description: str = "") -> None:
        """Log an earning."""
        self.logger.log_earning(amount, source, description)
