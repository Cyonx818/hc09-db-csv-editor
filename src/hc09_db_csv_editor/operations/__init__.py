"""Operations package - roster type strategies and registry.

This module provides the strategy registry that maps CSV headers
to their corresponding roster strategy implementations.
"""

from typing import Dict
from ..roster_strategy import RosterStrategy
from .player import PlayerStrategy
from .coach import CoachStrategy
from .gm import GMStrategy
from .trainer import TrainerStrategy
from ..constants import PLAYER_HEADER, COACH_HEADER, GM_HEADER, TRAINER_HEADER


class StrategyRegistry:
    """Registry for roster type strategies."""

    def __init__(self):
        """Initialize strategy registry with all roster types."""
        self._strategies: Dict[str, RosterStrategy] = {
            PLAYER_HEADER: PlayerStrategy(),    # PSA0
            COACH_HEADER: CoachStrategy(),      # CFDA
            GM_HEADER: GMStrategy(),            # GMAB
            TRAINER_HEADER: TrainerStrategy(),  # TRAB
        }

    def get_strategy(self, header: str) -> RosterStrategy:
        """Get strategy for given CSV header.

        Args:
            header: First CSV header field indicating roster type.

        Returns:
            RosterStrategy instance for the roster type.

        Raises:
            ValueError: If header doesn't match any known roster type.
        """
        if header not in self._strategies:
            raise ValueError(f"Unknown roster type header: {header}")
        return self._strategies[header]

    def get_roster_type_name(self, header: str) -> str:
        """Get roster type name from header.

        Args:
            header: First CSV header field indicating roster type.

        Returns:
            Human-readable roster type name.
        """
        return self.get_strategy(header).get_roster_type_name()


# Global registry instance
STRATEGY_REGISTRY = StrategyRegistry()
