"""Coach roster operations strategy.

This module implements the strategy for coach roster operations,
including general and positional coaching potential maximization.
"""

from typing import Dict, Callable, Tuple, Optional
import random
from ..roster_strategy import RosterStrategy
from ..models import Member, RosterContext
from ..constants import (
    MAXCOACHSTAT, MAXSKILLPOINTS,
    COACH_FIRST_NAME_CODE, COACH_LAST_NAME_CODE,
    COACH_POSITIONS
)


class CoachStrategy(RosterStrategy):
    """Strategy for coach roster operations."""

    def get_roster_type_name(self) -> str:
        return "Coach"

    def get_name_keys(self) -> Tuple[str, str]:
        return (COACH_FIRST_NAME_CODE, COACH_LAST_NAME_CODE)

    def supports_name_search(self) -> bool:
        return True

    def supports_bulk_operations(self) -> bool:
        return True

    def supports_name_randomization(self) -> bool:
        return True

    def get_skill_file_name(self) -> Optional[str]:
        return "cskl.csv"

    def get_individual_actions(self) -> Dict[str, Tuple[str, Callable]]:
        """Return coach individual action dictionary."""
        return {
            "1": ("Max General Coaching Potential", self.max_general_coaching_potential),
            "2": ("Max Positional Coaching Potential", self.max_positional_coaching_potential),
            "3": ("Read the Manual (Max Skill Points)", self.read_the_manual),
            "4": ("Take old boy out for drinks (Captain personality)", self.captain_personality),
            "5": ("Rename Coach", self.rename_coach),
            "6": ("Change Key Value", self.change_key_value),
        }

    def get_bulk_actions(self) -> Dict[str, Tuple[str, Callable]]:
        """Return coach bulk action dictionary."""
        return {
            "1": ("Max General Coaching Potential", self.max_general_coaching_potential),
            "2": ("Max Positional Coaching Potential", self.max_positional_coaching_potential),
            "3": ("Read the Manual (Max Skill Points)", self.read_the_manual),
            "4": ("Take old boy out for drinks (Captain personality)", self.captain_personality),
            "5": ("Change Key Value", self.change_key_value),
        }

    def list_by_team(self, context: RosterContext, ui) -> None:
        """Display coach roster listing for a team."""
        team_id = ui.prompt_team_id()
        if not team_id:
            return

        team_members = context.get_members_by_team(team_id)
        if not team_members:
            print(f"No coaches found for team ID {team_id}.")
            return

        print("\nCoach List:")
        line = ""
        for coach in team_members:
            pos_num = coach.data.get('COPS', '')
            position = COACH_POSITIONS.get(pos_num, "Unknown")
            first_name = coach.data.get(COACH_FIRST_NAME_CODE, '')
            last_name = coach.data.get(COACH_LAST_NAME_CODE, '')
            display_str = f"{position} {first_name} {last_name}"
            if len(line) + len(display_str) > 80:
                print(line)
                line = ""
            line += f"{display_str:<25}\t"
        if line:
            print(line)

    # Operation methods
    def max_general_coaching_potential(self, coach: Member) -> None:
        """Set general coaching stats to maximum value."""
        keys = ['SKPA', 'SKCM', 'SKSM', 'SKPX']
        for key in keys:
            coach.set_stat(key, MAXCOACHSTAT)

    def max_positional_coaching_potential(self, coach: Member, context: RosterContext = None) -> None:
        """Set positional coaching stats to maximum (requires skill file)."""
        if context is None or context.skill_members is None:
            print("Warning: No CSKL file found. Coach Positional editing not possible")
            return

        keys = ["SKIM", "SKPM", "SKLM"]
        for member in context.skill_members:
            if member.data["PNid"] == coach.data["PNid"]:
                for key in keys:
                    member.set_stat(key, MAXCOACHSTAT)

    def read_the_manual(self, coach: Member) -> None:
        """Set skill points to maximum value."""
        coach.set_stat('SKPT', MAXSKILLPOINTS)

    def captain_personality(self, coach: Member) -> None:
        """Set personality to captain (ID 9)."""
        coach.set_stat("PTId", 9)

    def rename_coach(self, coach: Member) -> None:
        """Prompt user to rename coach."""
        first_name = input("Enter new first name (case-sensitive): ").strip()
        last_name = input("Enter new last name (case-sensitive): ").strip()
        coach.data[COACH_FIRST_NAME_CODE] = first_name
        coach.data[COACH_LAST_NAME_CODE] = last_name

    def change_key_value(self, coach: Member, ui=None) -> None:
        """Prompt user to change a specific key value."""
        if ui is None:
            from ..ui import UI
            ui = UI()
        ui.prompt_key_value_change(coach)

    def randomize_names(self, context: RosterContext) -> None:
        """Randomize all coach names using existing name pool."""
        first_name_set = set()
        last_name_set = set()

        for coach in context.members:
            if COACH_FIRST_NAME_CODE in coach.data:
                first_name_set.add(coach.data[COACH_FIRST_NAME_CODE])
            if COACH_LAST_NAME_CODE in coach.data:
                last_name_set.add(coach.data[COACH_LAST_NAME_CODE])

        first_names = list(first_name_set)
        last_names = list(last_name_set)

        for coach in context.members:
            new_first_name = random.choice(first_names)
            coach.set_stat(COACH_FIRST_NAME_CODE, new_first_name)
            new_last_name = random.choice(last_names)
            coach.set_stat(COACH_LAST_NAME_CODE, new_last_name)

        context.mark_changed()
