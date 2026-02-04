"""Trainer roster operations strategy.

This module implements the strategy for trainer roster operations,
which are simpler than other roster types.
"""

from typing import Dict, Callable, Tuple, Optional
from ..roster_strategy import RosterStrategy
from ..models import Member, RosterContext
from ..constants import MAXGMSTAT, MAXSKILLPOINTS


class TrainerStrategy(RosterStrategy):
    """Strategy for trainer roster operations."""

    def get_roster_type_name(self) -> str:
        return "Trainer"

    def get_name_keys(self) -> Optional[Tuple[str, str]]:
        return None  # Trainers do not have editable names without PERV file

    def supports_name_search(self) -> bool:
        return False

    def supports_bulk_operations(self) -> bool:
        return False

    def supports_name_randomization(self) -> bool:
        return False

    def get_individual_actions(self) -> Dict[str, Tuple[str, Callable]]:
        """Return trainer individual action dictionary."""
        return {
            "1": ("Max Trainer Potential", self.max_trainer_potential),
            "2": ("Read the Manual (Max Skill Points)", self.read_the_manual),
            "3": ("Take old boy out for drinks (Captain personality)", self.captain_personality),
            "4": ("Change Key Value", self.change_key_value),
        }

    def get_bulk_actions(self) -> Dict[str, Tuple[str, Callable]]:
        """Return trainer bulk action dictionary (not used)."""
        return {}

    def list_by_team(self, context: RosterContext, ui) -> None:
        """Display trainer roster listing (not used for trainers)."""
        pass

    # Operation methods
    def max_trainer_potential(self, trainer: Member) -> None:
        """Set trainer stats to maximum value."""
        keys = ['TSIM', 'TSRM', 'TSFM']
        for key in keys:
            trainer.set_stat(key, MAXGMSTAT)

    def read_the_manual(self, trainer: Member) -> None:
        """Set skill points to maximum value."""
        trainer.set_stat('SKPT', MAXSKILLPOINTS)

    def captain_personality(self, trainer: Member) -> None:
        """Set personality to captain (ID 9)."""
        trainer.set_stat("PTId", 9)

    def change_key_value(self, trainer: Member, ui=None) -> None:
        """Prompt user to change a specific key value."""
        if ui is None:
            from ..ui import UI
            ui = UI()
        ui.prompt_key_value_change(trainer)

    def rename_trainer(self, trainer: Member) -> None:
        """Rename trainer (requires PERV file - not implemented)."""
        pass
