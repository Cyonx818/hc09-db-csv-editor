"""User interface functions for interactive CLI.

This module provides all user interaction functionality including
prompts, menus, team selection, and formatted output display.
"""

import argparse
import os
from typing import Optional, Callable, Dict, Tuple
from .models import Member
from .constants import TEAM_NAMES


class UI:
    """User interface handler for the application."""

    @staticmethod
    def get_input_file_path() -> str:
        """Get input file path from arguments or user prompt.

        Returns:
            Valid path to an existing CSV file.
        """
        parser = argparse.ArgumentParser(description="Process roster CSV file.")
        parser.add_argument('input_file', nargs='?', help="Path to the input CSV file.")
        args = parser.parse_args()

        if args.input_file and os.path.isfile(args.input_file):
            return args.input_file

        while True:
            file_path = input("Enter the path to the input CSV file: ").strip()
            if os.path.isfile(file_path):
                return file_path
            print("File not found. Please try again.")

    @staticmethod
    def print_team_names() -> None:
        """Display formatted team ID list in columns."""
        print("\nTeam ID List:")
        columns = 4
        col_width = 25
        teams_list = list(TEAM_NAMES.items())
        line = ""
        for i, (team_id, team_name) in enumerate(teams_list):
            formatted_id = f"{int(team_id):02d}"
            line += f"{formatted_id}: {team_name:<{col_width}}"
            if (i + 1) % columns == 0:
                print(line)
                line = ""
        if line:
            print(line)

    @staticmethod
    def prompt_team_id() -> str:
        """Prompt user for team ID selection.

        Returns:
            Valid team ID (1-33) or empty string if user quits.
        """
        UI.print_team_names()
        while True:
            team_id = input("\nEnter team ID (1-33, or 'q' to quit): ").strip()
            if team_id.lower() in ['q', 'quit']:
                return ''
            if team_id in TEAM_NAMES or team_id == '33':
                return team_id
            print(f"Invalid team ID: {team_id}. Please try again.")

    @staticmethod
    def prompt_name(roster_type: str) -> Optional[Tuple[str, str]]:
        """Prompt user for first and last name.

        Args:
            roster_type: Type of roster member (for display in prompt).

        Returns:
            Tuple of (first_name, last_name) or None if user quits.
        """
        first_name = input(f"Enter {roster_type}'s first name (or 'q' to quit): ").strip()
        if first_name.lower() in ['q', 'quit']:
            return None
        last_name = input(f"Enter {roster_type}'s last name (or 'q' to quit): ").strip()
        if last_name.lower() in ['q', 'quit']:
            return None
        return (first_name, last_name)

    @staticmethod
    def display_action_menu(actions: Dict[str, Tuple[str, Callable]], context_label: str) -> Optional[str]:
        """Display action menu and get user choice.

        Args:
            actions: Dictionary mapping choice keys to (description, function) tuples.
            context_label: Label for the quit option (e.g., "member selection").

        Returns:
            User's choice key or None if user quits.
        """
        print("\nChoose an action to perform:")
        for key, (description, _) in actions.items():
            print(f"{key}. {description}")
        print(f"q. Quit to {context_label}")

        choice = input("\nEnter your choice: ").strip().lower()
        return choice if choice not in ['q', 'quit'] else None

    @staticmethod
    def confirm_save(file_path: str) -> bool:
        """Prompt user to confirm save operation.

        Args:
            file_path: Path to the file being saved.

        Returns:
            True if user wants to save, False otherwise.
        """
        while True:
            response = input(f"Do you want to save changes to {file_path}? (yes/no): ").strip().lower()
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no']:
                return False
            print("Invalid input. Please enter 'yes' or 'no'.")

    @staticmethod
    def prompt_key_value_change(member: Member) -> None:
        """Prompt user to change a specific key value.

        Args:
            member: Member object to modify.
        """
        while True:
            key = input("Enter key name to change (4-character, case-sensitive, or 'q' to quit): ").strip()
            if key.lower() in ['q', 'quit']:
                return
            if len(key) != 4:
                print("Invalid key name. It must be a 4-character string.")
                continue
            if key in member.data:
                print(f"Current value for {key}: {member.data[key]}")
                new_value = input(f"Enter new value for {key}: ").strip()
                member.set_stat(key, new_value)
                return
            else:
                print(f"Key '{key}' not found. Please try again.")
