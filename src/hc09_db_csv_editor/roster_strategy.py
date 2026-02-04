"""Abstract base class for roster type strategies.

This module defines the interface that all roster type strategies must implement.
The Strategy Pattern allows different roster types to provide type-specific
operations while sharing common infrastructure.
"""

from abc import ABC, abstractmethod
from typing import Dict, Callable, List, Optional, Tuple


class RosterStrategy(ABC):
    """Abstract base class defining interface for roster type operations."""

    @abstractmethod
    def get_roster_type_name(self) -> str:
        """Return human-readable roster type name.

        Returns:
            Name of the roster type (e.g., 'Player', 'Coach').
        """
        pass

    @abstractmethod
    def get_individual_actions(self) -> Dict[str, Tuple[str, Callable]]:
        """Return action dictionary for individual member operations.

        Returns:
            Dictionary mapping action keys to (description, function) tuples.
        """
        pass

    @abstractmethod
    def get_bulk_actions(self) -> Dict[str, Tuple[str, Callable]]:
        """Return action dictionary for bulk team operations.

        Returns:
            Dictionary mapping action keys to (description, function) tuples.
        """
        pass

    @abstractmethod
    def supports_name_search(self) -> bool:
        """Whether this roster type supports name-based search.

        Returns:
            True if members can be searched by name, False otherwise.
        """
        pass

    @abstractmethod
    def supports_bulk_operations(self) -> bool:
        """Whether this roster type supports bulk team operations.

        Returns:
            True if bulk operations are available, False otherwise.
        """
        pass

    @abstractmethod
    def get_name_keys(self) -> Optional[Tuple[str, str]]:
        """Return (first_name_key, last_name_key) tuple or None.

        Returns:
            Tuple of CSV field names for first and last name, or None if
            this roster type doesn't support name access.
        """
        pass

    @abstractmethod
    def list_by_team(self, context, ui) -> None:
        """Display roster listing for a team (type-specific formatting).

        Args:
            context: RosterContext containing members and state.
            ui: UI instance for user interaction.
        """
        pass

    def get_skill_file_name(self) -> Optional[str]:
        """Return companion skill file name or None.

        Returns:
            Name of skill file (e.g., 'cskl.csv') or None if not applicable.
        """
        return None

    def supports_name_randomization(self) -> bool:
        """Whether this roster type supports name randomization.

        Returns:
            True if name randomization is available, False otherwise.
        """
        return False
