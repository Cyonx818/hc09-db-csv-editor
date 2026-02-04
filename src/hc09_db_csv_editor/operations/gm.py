"""GM roster operations strategy.

This module implements the strategy for GM roster operations,
including general and positional GM potential maximization.
"""

from typing import Dict, Callable, Tuple, Optional
from ..roster_strategy import RosterStrategy
from ..models import Member, RosterContext
from ..constants import MAXGMSTAT, MAXSKILLPOINTS


class GMStrategy(RosterStrategy):
    """Strategy for GM roster operations."""

    def get_roster_type_name(self) -> str:
        return "GM"

    def get_name_keys(self) -> Optional[Tuple[str, str]]:
        return None  # GMs do not have editable names without PERV file

    def supports_name_search(self) -> bool:
        return False

    def supports_bulk_operations(self) -> bool:
        return False

    def supports_name_randomization(self) -> bool:
        return False

    def get_skill_file_name(self) -> Optional[str]:
        return "gmsk.csv"

    def get_individual_actions(self) -> Dict[str, Tuple[str, Callable]]:
        """Return GM individual action dictionary."""
        return {
            "1": ("Max General GM Potential", self.max_general_gm_potential),
            "2": ("Max Positional GM Potential", self.max_positional_gm_potential),
            "3": ("Read the Manual (Max Skill Points)", self.read_the_manual),
            "4": ("Take old boy out for drinks (Captain personality)", self.captain_personality),
            "5": ("Change Key Value", self.change_key_value),
        }

    def get_bulk_actions(self) -> Dict[str, Tuple[str, Callable]]:
        """Return GM bulk action dictionary (not used)."""
        return {}

    def list_by_team(self, context: RosterContext, ui) -> None:
        """Display GM roster listing (not used for GMs)."""
        pass

    # Operation methods
    def max_general_gm_potential(self, gm: Member) -> None:
        """Set general GM stats to maximum value."""
        keys = ['SKTM', 'SKTD', 'SKNM', 'SKNG']
        for key in keys:
            gm.set_stat(key, MAXGMSTAT)

    def max_positional_gm_potential(self, gm: Member, context: RosterContext = None) -> None:
        """Set positional GM stats to maximum (requires skill file)."""
        if context is None or context.skill_members is None:
            print("Warning: No GMSK file found. GM Positional editing not possible.")
            return

        keys = ["SKRM", "SKSX"]
        for member in context.skill_members:
            if member.data["PNid"] == gm.data["PNid"]:
                for key in keys:
                    member.set_stat(key, MAXGMSTAT)

    def read_the_manual(self, gm: Member) -> None:
        """Set skill points to maximum value."""
        gm.set_stat('SKPT', MAXSKILLPOINTS)

    def captain_personality(self, gm: Member) -> None:
        """Set personality to captain (ID 9)."""
        gm.set_stat("PTId", 9)

    def change_key_value(self, gm: Member, ui=None) -> None:
        """Prompt user to change a specific key value."""
        if ui is None:
            from ..ui import UI
            ui = UI()
        ui.prompt_key_value_change(gm)

    def rename_gm(self, gm: Member) -> None:
        """Rename GM (requires PERV file - not implemented)."""
        pass
