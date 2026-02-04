"""Player roster operations strategy.

This module implements the strategy for player roster operations,
including stat maximization, contract manipulation, and name operations.
"""

from typing import Dict, Callable, Tuple
import random
from ..roster_strategy import RosterStrategy
from ..models import Member, RosterContext
from ..constants import (
    MAXPLAYERSTAT, MAXHEALTH, MINPLRN,
    PLAYER_FIRST_NAME_CODE, PLAYER_LAST_NAME_CODE,
    PLAYER_STATS, PLAYER_POSITIONS
)


class PlayerStrategy(RosterStrategy):
    """Strategy for player roster operations."""

    def get_roster_type_name(self) -> str:
        return "Player"

    def get_name_keys(self) -> Tuple[str, str]:
        return (PLAYER_FIRST_NAME_CODE, PLAYER_LAST_NAME_CODE)

    def supports_name_search(self) -> bool:
        return True

    def supports_bulk_operations(self) -> bool:
        return True

    def supports_name_randomization(self) -> bool:
        return True

    def get_individual_actions(self) -> Dict[str, Tuple[str, Callable]]:
        """Return player individual action dictionary."""
        return {
            "1": ("Maximize Potential", self.max_potential),
            "2": ("Maximize Health", self.max_health),
            "3": ("Resign for Peanuts (7yr contract at league minimum salary)", self.resign_for_peanuts),
            "4": ("Make Physical Specimen (increase physical size & max potentials)", self.make_physical_specimen),
            "5": ("Take 'roids (inflate current stats)", self.inflate_current_stats),
            "6": ("Rename Player", self.rename_player),
            "7": ("Change Key Value", self.change_key_value),
        }

    def get_bulk_actions(self) -> Dict[str, Tuple[str, Callable]]:
        """Return player bulk action dictionary."""
        return {
            "1": ("Maximize Potential", self.max_potential),
            "2": ("Maximize Health", self.max_health),
            "3": ("Resign for Peanuts (7yr contract at league minimum salary)", self.resign_for_peanuts),
            "4": ("Make Physical Specimen (increase physical size & max potentials)", self.make_physical_specimen),
            "5": ("Take 'roids (inflate current stats)", self.inflate_current_stats),
            "6": ("Change Key Value", self.change_key_value),
        }

    def list_by_team(self, context: RosterContext, ui) -> None:
        """Display player roster listing for a team."""
        team_id = ui.prompt_team_id()
        if not team_id:
            return

        team_members = context.get_members_by_team(team_id)
        if not team_members:
            print(f"No players found for team ID {team_id}.")
            return

        print("\nPlayer List:")
        line = ""
        for player in team_members:
            pos_num = player.data.get('PPOS', '')
            position = PLAYER_POSITIONS.get(pos_num, "Unknown")
            first_name = player.data.get(PLAYER_FIRST_NAME_CODE, '')
            last_name = player.data.get(PLAYER_LAST_NAME_CODE, '')
            display_str = f"{position} {first_name} {last_name}"
            if len(line) + len(display_str) > 80:
                print(line)
                line = ""
            line += f"{display_str:<25}\t"
        if line:
            print(line)

    # Operation methods
    def max_potential(self, player: Member) -> None:
        """Set all potential stats to maximum value."""
        for key in player.data:
            if key.endswith('x') or key.endswith('X'):
                current_value = int(player.data[key])
                if current_value > MAXPLAYERSTAT:
                    new_value = MAXHEALTH
                else:
                    new_value = MAXPLAYERSTAT
                player.set_stat(key, new_value)

    def max_health(self, player: Member) -> None:
        """Set all health/durability stats to maximum value."""
        health_keys = ['PLAC', 'PRAC', 'PHDC', 'PLLC', 'PTRC', 'PRLc', 'PSTA', 'PTGH', 'PINJ']
        for key in health_keys:
            if key in player.data:
                current_value = int(player.data[key])
                if current_value > MAXPLAYERSTAT:
                    new_value = MAXHEALTH
                else:
                    new_value = MAXPLAYERSTAT
                player.set_stat(key, new_value)
        if int(player.data['PLRN']) < MINPLRN:
            player.set_stat('PLRN', MINPLRN)

    def inflate_current_stats(self, player: Member) -> None:
        """Increase player's stats by half the difference to potential max."""
        for stat, max_key in PLAYER_STATS.items():
            player_stat = int(player.data[stat])
            player_stat_max = int(player.data[max_key])
            if player_stat < player_stat_max:
                inflation_amount = (player_stat_max - player_stat) // 2
            else:
                inflation_amount = 0
            inflated_value = player_stat + inflation_amount
            player.set_stat(stat, inflated_value)

    def resign_for_peanuts(self, player: Member) -> None:
        """Set contract to 7 years at league minimum with captain personality."""
        salary_key_value_dict = {
            'PSA0': 24,
            'PSA1': 24,
            'PSA2': 24,
            'PSA3': 24,
            'PSA4': 24,
            'PSA5': 24,
            'PSA6': 24,
            'PSB0': 0,
            'PSB1': 0,
            'PSB2': 0,
            'PSB3': 0,
            'PSB4': 0,
            'PSB5': 0,
            'PSB6': 0,
            'PCSA': 24,
            'PTSA': 168,
            'PVSB': 0,
            'PCYL': 7,
            'PCON': 7,
            'PSBO': 0,
            'PVCO': 0,
            'PFHO': 0,
            'PTId': 9,
        }
        for key, new_value in salary_key_value_dict.items():
            if key in player.data:
                player.set_stat(key, new_value)

    def make_physical_specimen(self, player: Member) -> None:
        """Set age to 21 and increase height/weight by 10%."""
        player.set_stat('PAGE', 21)

        current_height = player.data.get('PHGT', 0)
        current_weight = player.data.get('PWGT', 0)
        new_height = int(float(current_height) * 1.1)
        new_weight = int(float(current_weight) * 1.1)
        player.set_stat('PHGT', new_height)
        player.set_stat('PWGT', new_weight)

    def rename_player(self, player: Member) -> None:
        """Prompt user to rename player."""
        first_name = input("Enter new first name (case-sensitive): ").strip()
        last_name = input("Enter new last name (case-sensitive): ").strip()
        player.set_stat(PLAYER_FIRST_NAME_CODE, first_name)
        player.set_stat(PLAYER_LAST_NAME_CODE, last_name)

    def change_key_value(self, player: Member, ui=None) -> None:
        """Prompt user to change a specific key value."""
        if ui is None:
            from ..ui import UI
            ui = UI()
        ui.prompt_key_value_change(player)

    def randomize_names(self, context: RosterContext) -> None:
        """Randomize all player names using existing name pool."""
        first_name_set = set()
        last_name_set = set()

        for player in context.members:
            if PLAYER_FIRST_NAME_CODE in player.data:
                first_name_set.add(player.data[PLAYER_FIRST_NAME_CODE])
            if PLAYER_LAST_NAME_CODE in player.data:
                last_name_set.add(player.data[PLAYER_LAST_NAME_CODE])

        first_names = list(first_name_set)
        last_names = list(last_name_set)

        for player in context.members:
            new_first_name = random.choice(first_names)
            player.set_stat(PLAYER_FIRST_NAME_CODE, new_first_name)
            new_last_name = random.choice(last_names)
            player.set_stat(PLAYER_LAST_NAME_CODE, new_last_name)

        context.mark_changed()
