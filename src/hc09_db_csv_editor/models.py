"""Data models for roster members and application context.

This module defines the core data structures used throughout the application,
including the Member class for individual roster entries and RosterContext
for managing application state without global variables.
"""

from typing import Dict, List, Optional


class Member:
    """Represents a single roster entry (player/coach/GM/trainer).

    This class wraps a dictionary of CSV data and provides convenient
    methods for accessing and modifying member attributes.
    """

    def __init__(self, data: Dict[str, str]):
        """Initialize a Member with CSV row data.

        Args:
            data: Dictionary mapping CSV field names to values.
        """
        self.data = data

    def set_stat(self, stat_key: str, value) -> None:
        """Set a stat value.

        Args:
            stat_key: The CSV field name to update.
            value: The new value (will be converted to string).
        """
        if stat_key in self.data:
            self.data[stat_key] = str(value)
        else:
            print(f"Stat {stat_key} does not exist.")

    def get_stat(self, stat_key: str, default=None):
        """Get a stat value with optional default.

        Args:
            stat_key: The CSV field name to retrieve.
            default: Value to return if key doesn't exist.

        Returns:
            The stat value or default if not found.
        """
        return self.data.get(stat_key, default)

    def get_name(self, first_name_key: str, last_name_key: str) -> str:
        """Get formatted name from specified keys.

        Args:
            first_name_key: CSV field name for first name.
            last_name_key: CSV field name for last name.

        Returns:
            Formatted full name (first + last).
        """
        first = self.data.get(first_name_key, '')
        last = self.data.get(last_name_key, '')
        return f"{first} {last}".strip()


class RosterContext:
    """Container for application state.

    This class replaces global variables and provides a clean way to pass
    application state through function calls.
    """

    def __init__(self,
                 roster_type: str,
                 members: List[Member],
                 headers: List[str],
                 file_path: str,
                 skill_members: Optional[List[Member]] = None,
                 skill_headers: Optional[List[str]] = None,
                 skill_file_path: Optional[str] = None):
        """Initialize application context.

        Args:
            roster_type: Type of roster (Player, Coach, GM, Trainer).
            members: List of Member objects from main CSV.
            headers: CSV headers from main file.
            file_path: Path to main CSV file.
            skill_members: Optional list of Member objects from skill file.
            skill_headers: Optional CSV headers from skill file.
            skill_file_path: Optional path to skill file.
        """
        self.roster_type = roster_type
        self.members = members
        self.headers = headers
        self.file_path = file_path
        self.skill_members = skill_members
        self.skill_headers = skill_headers
        self.skill_file_path = skill_file_path
        self.changes_made = False

    def mark_changed(self) -> None:
        """Mark that changes have been made to the roster."""
        self.changes_made = True

    def get_members_by_team(self, team_id: str) -> List[Member]:
        """Filter members by team ID.

        Args:
            team_id: Team ID to filter by (1-33, where 33 is Free Agents).

        Returns:
            List of members belonging to the specified team.
        """
        if team_id == "33":  # Free Agents
            return [m for m in self.members if m.data['TGID'] not in map(str, range(1, 33))]
        return [m for m in self.members if m.data.get('TGID') == team_id]
