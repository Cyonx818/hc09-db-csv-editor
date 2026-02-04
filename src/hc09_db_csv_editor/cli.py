"""Command-line interface orchestration.

This module provides the main application controller that coordinates
between UI, I/O operations, and roster strategies.
"""

from typing import Optional
from .models import RosterContext, Member
from .io_handler import IOHandler
from .ui import UI
from .operations import STRATEGY_REGISTRY


class Application:
    """Main application controller."""

    def __init__(self):
        """Initialize application with required components."""
        self.io_handler = IOHandler()
        self.ui = UI()
        self.strategy_registry = STRATEGY_REGISTRY

    def run(self) -> None:
        """Main application entry point."""
        # Get input file
        file_path = self.ui.get_input_file_path()

        # Load roster data
        headers, members = self.io_handler.read_csv(file_path)

        # Detect roster type and get strategy
        strategy = self.strategy_registry.get_strategy(headers[0])
        roster_type = strategy.get_roster_type_name()
        print(f"Detected roster type: {roster_type}")

        # Load skill file if needed
        skill_members = None
        skill_headers = None
        skill_file_path = None
        skill_file_name = strategy.get_skill_file_name()
        if skill_file_name:
            skill_file_path = self.io_handler.find_skill_file(file_path, skill_file_name)
            if skill_file_path:
                print(f"{skill_file_name} found at {skill_file_path}!")
                skill_headers, skill_members = self.io_handler.read_csv(skill_file_path)
            else:
                print(f"{skill_file_name} not found. Editing positional stats is impossible!")

        # Create context
        context = RosterContext(
            roster_type=roster_type,
            members=members,
            headers=headers,
            file_path=file_path,
            skill_members=skill_members,
            skill_headers=skill_headers,
            skill_file_path=skill_file_path
        )

        # Run main menu loop
        self.main_menu(context, strategy)

        # Save changes if needed
        if context.changes_made:
            self.save_changes(context)

    def main_menu(self, context: RosterContext, strategy) -> None:
        """Main menu loop.

        Args:
            context: Application state container.
            strategy: Roster strategy for current roster type.
        """
        while True:
            print(f"\n=== Main Menu: {context.roster_type} Roster ===")

            # Build dynamic menu based on strategy capabilities
            menu_options = []
            choice_map = {}

            if strategy.supports_name_search():
                menu_options.append(f"1. List all {context.roster_type}s on a team")
                choice_map['1'] = 'list'
                menu_options.append(f"2. Select a {context.roster_type} by name")
                choice_map['2'] = 'select_by_name'

                if strategy.supports_bulk_operations():
                    menu_options.append(f"3. Modify all {context.roster_type}s on a team")
                    choice_map['3'] = 'modify_team'

                if strategy.supports_name_randomization():
                    menu_options.append(f"4. Randomize {context.roster_type} names (warning, this will affect all {context.roster_type}s!)")
                    choice_map['4'] = 'randomize'
            else:
                # GM/Trainer - simple menu
                menu_options.append(f"1. Select a {context.roster_type} by team")
                choice_map['1'] = 'select_by_team'

            menu_options.append("q. Quit")

            for option in menu_options:
                print(option)

            choice = input("\nEnter your choice: ").strip().lower()

            if choice in ['q', 'quit']:
                break
            elif choice in choice_map:
                action = choice_map[choice]
                if action == 'list':
                    strategy.list_by_team(context, self.ui)
                elif action == 'select_by_name':
                    self.select_by_name(context, strategy)
                elif action == 'modify_team':
                    self.modify_team(context, strategy)
                elif action == 'randomize':
                    self.randomize_names(context, strategy)
                elif action == 'select_by_team':
                    self.select_by_team(context, strategy)
            else:
                print("Invalid choice. Please try again.")

    def select_by_name(self, context: RosterContext, strategy) -> None:
        """Select and modify a member by name.

        Args:
            context: Application state container.
            strategy: Roster strategy for current roster type.
        """
        while True:
            name_tuple = self.ui.prompt_name(context.roster_type)
            if name_tuple is None:
                break

            first_name, last_name = name_tuple
            member_index = self.find_member_index(context.members, first_name, last_name, strategy)

            if member_index is not None:
                self.modify_individual(context, strategy, context.members[member_index])
                break
            else:
                print(f"{context.roster_type} not found. Please try again.")

    def select_by_team(self, context: RosterContext, strategy) -> None:
        """Select and modify a member by team (for GM/Trainer).

        Args:
            context: Application state container.
            strategy: Roster strategy for current roster type.
        """
        print(f"Which team's {context.roster_type} do you want to edit?")
        self.ui.print_team_names()
        team_id = input("\nEnter team ID (1-33): ").strip()

        team_members = context.get_members_by_team(team_id)

        if not team_members:
            print(f"No {context.roster_type} found for team ID {team_id}.")
            return

        member = team_members[0]
        self.modify_individual(context, strategy, member)

    def modify_individual(self, context: RosterContext, strategy, member: Member) -> None:
        """Modify an individual member.

        Args:
            context: Application state container.
            strategy: Roster strategy for current roster type.
            member: Member to modify.
        """
        actions = strategy.get_individual_actions()
        member_type = context.roster_type.lower()
        if member_type == "gm":
            member_type = "GM"

        while True:
            print("\nChoose an action to perform:")
            for key, (description, _) in actions.items():
                print(f"{key}. {description}")
            print(f"q. Quit to {member_type} selection")

            choice = input("\nEnter the number of your choice: ").strip().lower()
            if choice in actions:
                _, action = actions[choice]
                # Call action with context if it accepts it
                try:
                    action(member, context)
                except TypeError:
                    # Fallback for actions that don't need context
                    action(member)
                context.mark_changed()
                print(f"Action '{actions[choice][0]}' performed on {member_type}.")
            elif choice in ['q', 'quit']:
                break
            else:
                print("Invalid choice. Please try again.")

    def modify_team(self, context: RosterContext, strategy) -> None:
        """Modify all members on a team.

        Args:
            context: Application state container.
            strategy: Roster strategy for current roster type.
        """
        self.ui.print_team_names()
        while True:
            team_id = input(f"Enter team to bulk edit {context.roster_type}s (or 'q' to quit): ").strip()
            if team_id.lower() in ['q', 'quit']:
                break
            elif team_id:
                self.modify_bulk_members(context, strategy, team_id)
                break

    def modify_bulk_members(self, context: RosterContext, strategy, team_id: str) -> None:
        """Apply bulk operations to team members.

        Args:
            context: Application state container.
            strategy: Roster strategy for current roster type.
            team_id: Team ID to operate on.
        """
        actions = strategy.get_bulk_actions()

        while True:
            print("\nChoose an action to perform:")
            for key, (description, _) in actions.items():
                print(f"{key}. {description}")
            print(f"q. Quit to {context.roster_type} selection")

            choice = input("\nEnter the number of your choice: ").strip().lower()
            if choice in actions:
                _, action = actions[choice]
                for member in context.members:
                    if member.data['TGID'] == team_id:
                        # Call action with context if it accepts it
                        try:
                            action(member, context)
                        except TypeError:
                            # Fallback for actions that don't need context
                            action(member)
                        context.mark_changed()
                        name_keys = strategy.get_name_keys()
                        if name_keys:
                            member_name = member.get_name(name_keys[0], name_keys[1])
                            print(f"Action '{actions[choice][0]}' performed on {context.roster_type} {member_name}.")
                        else:
                            print(f"Action '{actions[choice][0]}' performed on {context.roster_type}.")
            elif choice in ['q', 'quit']:
                break
            else:
                print("Invalid choice. Please try again.")

    def randomize_names(self, context: RosterContext, strategy) -> None:
        """Randomize all member names.

        Args:
            context: Application state container.
            strategy: Roster strategy for current roster type.
        """
        strategy.randomize_names(context)

    def find_member_index(self, members, first_name: str, last_name: str, strategy) -> Optional[int]:
        """Find member index by name.

        Args:
            members: List of members to search.
            first_name: First name to search for.
            last_name: Last name to search for.
            strategy: Roster strategy (provides name keys).

        Returns:
            Index of member if found, None otherwise.
        """
        name_keys = strategy.get_name_keys()
        if name_keys is None:
            return None

        first_name_key, last_name_key = name_keys
        for i, member in enumerate(members):
            if (member.data[first_name_key].lower() == first_name.lower() and
                member.data[last_name_key].lower() == last_name.lower()):
                return i
        return None

    def save_changes(self, context: RosterContext) -> None:
        """Prompt to save changes.

        Args:
            context: Application state container.
        """
        if self.ui.confirm_save(context.file_path):
            output_file = self.io_handler.write_csv(context.members, context.headers, context.file_path)
            print(f"Changes saved to {output_file}")

            if context.skill_file_path and context.skill_members:
                skill_output = self.io_handler.write_csv(
                    context.skill_members,
                    context.skill_headers,
                    context.skill_file_path
                )
                print(f"Skill file changes saved to {skill_output}")
        else:
            print("Changes not saved.")


def main() -> None:
    """Entry point for the application."""
    app = Application()
    app.run()
